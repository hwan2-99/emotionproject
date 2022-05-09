import cv2
import base64

import numpy as np
import pymongo as mongo
from tensorflow import keras
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from uuid import uuid4
from time import sleep
from tkinter import *
from PIL import ImageTk, Image
import base64
import os


def faceEmotion(id, image):
    # 얼굴 감지 XML로드 및 훈련 된 모델로드
    print(id, "아이디")
    emotion_classifier = load_model(os.getcwd() + '/faceEmotion/files/emotion_model.hdf5', compile=False)
    face_detection = cv2.CascadeClassifier(os.getcwd() + '/faceEmotion/files/haarcascade_frontalface_default.xml')

    EMOTIONS = ["Angry", "Disgusting", "Fearful", "Happy", "Sad", "Surpring", "Neutral"]

    client1 = mongo.MongoClient()
    # 호스트와 포트를 지정
    client2 = mongo.MongoClient('localhost', 27017)
    # URL로 호스트와 포트를 지정
    client3 = mongo.MongoClient('mongodb://localhost:27017/')
    # 데이터베이스를 생성 혹은 지정
    db = client1.face  # db = client1["dsdb"]
    db2 = client1.emotionPicture
    DBSad = db[id]
    t = DBSad.find()
    count = 0;
    ave = 0;
    # for x in t:
    #     ave += x['Face_Fearful']
    #     count = count + 1;

    if count < 10:
        ave = 0.2
    else:
        ave = ave / count
        print(ave)
    # 웹캠을 사용한 비디오 캡처

    i = 1;
    count = 1;

    while True:
        # 카메라에서 이미지 캡처
        gray = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE);
        # ret, frame = camera.read()

        # 색상을 그레이 스케일로 변환
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 프레임 내 얼굴 인식
        faces = face_detection.detectMultiScale(gray,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(30, 30))

        # 얼굴이 감지 될 때만 감정 인식을 수행합니다.
        if len(faces) > 0:
            # 가장 큰 이미지
            face = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = face
            # 신경망을 위해 이미지 크기를 48x48로 조정합니다.
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # 감정 예측
            preds = emotion_classifier.predict(roi)[0]
            emotion_probability = np.max(preds)
            label = EMOTIONS[preds.argmax()]

            Angry = preds[0]
            Disgusting = preds[1]
            Fearful = float(preds[2])
            Happy = preds[3]
            Sad = preds[4]
            Surprise = preds[5]
            Neutral = preds[6]
            print("동작중입니다.")
            if (Fearful > ave):
                print("Angry", Angry);
                print("Disgusting", Disgusting)
                print("Fearful", Fearful)
                print("Happy", Happy)
                print("Sad", Sad)
                print("Surprise", Surprise)
                print("Neutral", Neutral)

                # 사진 저장 이름은 UUID로 임의값으로 저장
                uuid_name = uuid4().hex;
                file_name_path = 'faceEmotion/faces/' + uuid_name + '.jpg';
                cv2.imwrite(file_name_path, image)
                data2 = {id: file_name_path}
                data = {id: round(Fearful, 2)}

                # DBSad.insert_one(data)
                # DBPicture.insert_one(data2)
                return 'no', float(Fearful), float(Angry), float(Disgusting), float(Happy), float(Sad), float(Surprise), float(Neutral)

            else:
                return 'yes', float(Fearful), float(Angry), float(Disgusting), float(Happy), float(Sad), float(Surprise), float(Neutral)
        else:
            return 'no', 0, 0, 0, 0, 0, 0, 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
