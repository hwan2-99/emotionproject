import cv2
import numpy as np
import os
import io
from PIL import Image
from os import listdir
from os.path import isfile, join
from uuid import uuid4
face_classifier = cv2.CascadeClassifier('faceEmotion/haarcascade_frontalface_default.xml')


def face_extractor(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    if faces is():
        return None

    for(x,y,w,h) in faces:
        cropped_face = img[y:y+h, x:x+w]

    return cropped_face


def myface(image,user):
    data_path = 'faces/'+user+"/"

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    Training_Data, Labels = [], []

    dataBytesIO = io.BytesIO(image)
    image2 = Image.open(dataBytesIO);

    if face_extractor(np.array(image2)) is not None:
        value = len(os.listdir(data_path))
        if value > 30:

            for i, files in enumerate(onlyfiles):
                image_path = data_path + onlyfiles[i]
                images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                Training_Data.append(np.asarray(images, dtype=np.uint8))
                Labels.append(i)

            Labels = np.asarray(Labels, dtype=np.int32)
            model = cv2.face.LBPHFaceRecognizer_create()

            model.train(np.asarray(Training_Data), np.asarray(Labels))

            print("Model Training Complete!!!!!")

            face = cv2.cvtColor(np.array(image2), cv2.COLOR_BGR2GRAY)
            result = model.predict(face)

            confidence = int(100 * (1 - (result[1]) / 300))
            print("정확도는 : ?", confidence)
            if confidence < 50 :
                return "X"


        face = cv2.resize(face_extractor(np.array(image2)), (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        uuid_name = uuid4().hex;
        file_name_path = data_path + uuid_name + '.jpg'
        cv2.imwrite(file_name_path,face);
        return "O";
