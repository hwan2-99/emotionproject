import json

from django.shortcuts import render

# Create your views here.
import datetime
import numpy as np
import base64
import pymongo as mongo
from datetime import date

from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from voiceEmotion.main import emotionCheck
from faceEmotion.face_Recognition import myface
from django import http
import wave
from faceEmotion.face import faceEmotion
# sqlite3 모델들
from emotionSys.models import User, AuthSms, Auth_Category, AuthEmail, Emotion, EncryptionAlgorithm, ChoiceCheck

from Crypto.Cipher import Salsa20

@csrf_exempt
@api_view(['GET', 'POST'])
def voice(request):
    if request.method == "POST":

        # 음성 서버에 저장하는 작업
        audio_file = request.FILES.get('audio_data', None)

        obj = wave.open(audio_file, 'r')
        audio = wave.open('voiceEmotion/test.wav', 'wb')
        audio.setnchannels(obj.getnchannels())
        audio.setnframes(obj.getnframes())
        audio.setsampwidth(obj.getsampwidth())
        audio.setframerate(obj.getframerate())
        blob = audio_file.read()
        audio.writeframes(blob)

        voiceresult = emotionCheck()

        print("hello voice")
        id = request.session.get("user_email")
        today = date.today()
        uuid_name = uuid4().hex

        data_json = {
            '_id': uuid_name,
            'positive': voiceresult['neutral'],
            'negative': voiceresult['fear'],
            'date': str(datetime.datetime.now())
        }

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.voice
        DBVoice = db[id]
        DBVoice.insert_one(data_json)

        client2 = mongo.MongoClient()
        db2 = client2.voice_count
        DBVoice_Count = db2[id]
        DBVoice_Count.update({'_id': id}, {
            '$inc': {'positive_cnt': 1},
        }, upsert=True)
        DBVoice_Count.update({'_id': id}, {
            '$inc': {'negative_cnt': 1},
        }, upsert=True)

        if voiceresult['fear'] >= 0.5:
            db2 = client1.fail
            dbfail = db2[id]
            data = {
                "_id": uuid_name,
                "detection": "voice",
                "result": voiceresult['fear'],
                "date": str(datetime.datetime.now())
            }
            dbfail.insert_one(data)

        print(data_json)
        return Response({'data': data_json}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def face(request):
    #
    # id = request.session.get("user")
    image = request.POST['faceURL'].split(',')[1]
    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data, np.uint8)


    id = request.session.get("user_email")
    result = myface(np_data,id)
    today = date.today()
    uuid_name = uuid4().hex;
    data_json = {
        "_id": uuid_name,
        "neutral": request.POST['neutral'],
        "happy": request.POST['happy'],
        "neutral": request.POST['neutral'],
        "angry": request.POST['angry'],
        "sad": request.POST['sad'],
        "fearful": request.POST['fearful'],
        "Date": str(datetime.datetime.now())
    }
    print("hello face")
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db = client1.face
    DBFace = db[id]
    DBFace.insert_one(data_json)

    if float(request.POST['fearful']) >= 0.2:
        print("fearful Test ~~~~~~~~~~~~~~~~~~")
        db2 = client1.fail
        dbfail = db2[id]
        data = {
            "_id": uuid_name,
            "detection": "face",
            "result": request.POST['fearful'],
            "date": str(datetime.datetime.now())
        }
        dbfail.insert_one(data)

    print(data_json)
    return Response({'data': data_json, 'face': result}, status=status.HTTP_200_OK)


@api_view(['UPDATE'])
def mypage_emotion(request):
    if request.method == "UPDATE":
        # voiceresult = emotionCheck()
        # faceresult = faceEmotion()

        # 사용자 아이디 조회를 통하여 보안 속성 가져오기

        # 만약 설정 조건이 맞을 경우 return 200

        # 아닐 경우 return 400

        return Response("ok", status=status.HTTP_200_OK)


@api_view(['GET','PATCH'])
def choice_check(request):
    if request.method == "GET":
        email = request.GET.get('email')
        choiceCheck = ChoiceCheck.objects.get(email=email)

        return Response(choiceCheck.choice, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        email = request.data['email']
        settingNum = request.data['settingNum']
        choiceCheck = ChoiceCheck.objects.get(email=email)
        choiceCheck.choice = settingNum
        choiceCheck.save()
        return Response('ok', status=status.HTTP_200_OK)

@api_view(['GET','PATCH'])
def encryption_algorithm(request):
    if request.method == "GET":
        email = request.GET.get('email')
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=email)
        return Response(encryptionAlgorithm.choice, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        email = request.data['email']
        settingNum = request.data['settingNum']
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=email)
        encryptionAlgorithm.choice = settingNum
        encryptionAlgorithm.save()
        return Response('ok', status=status.HTTP_200_OK)