import json

from django.shortcuts import render

# Create your views here.
import datetime
import numpy as np
import base64
import pymongo as mongo
import json
from datetime import date
from datetime import datetime
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
from emotionSys.models import EncryptionAlgorithm, ChoiceCheck

from Crypto import Random
from Crypto.Cipher import AES

adminEmail = 'admin@gmail.com'

key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
        0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]
BS = 16
pad = lambda s: s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class AESCipher:
    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf-8') ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

@csrf_exempt
@api_view(['GET', 'POST'])
def voice(request):
    # today = date.today()

    encrypt_startTime = datetime.now()

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

        uuid_name = uuid4().hex

        data_json = {
            '_id': uuid_name,
            'positive': voiceresult['neutral'],
            'negative': voiceresult['fear'],
            'date': str(datetime.datetime.now())
        }

        # json 데이터 직렬화
        json_data = json.dumps(data_json)
        # 암호화
        encrypted_data = AESCipher(bytes(key)).encrypt(json_data)

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.voice
        DBVoice = db[id]

        DBVoice.insert_one({
            'encrypted_data': encrypted_data,
            'date': data_json['date']
        })

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

        print(encrypted_data)
        encrypt_endTime = datetime.now()

        encrypt_Time = encrypt_endTime - encrypt_startTime


        return Response({'data': data_json}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def face(request):
    # today = date.today()
    # id = request.session.get("user")

    image = request.POST['faceURL'].split(',')[1]
    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data, np.uint8)

    id = request.session.get("user_email")
    result = myface(np_data,id)

    uuid_name = uuid4().hex
    data_json = {
         "_id": uuid_name,
        "neutral": request.POST['neutral'],
        "happy": request.POST['happy'],
        "angry": request.POST['angry'],
        "sad": request.POST['sad'],
        "fearful": request.POST['fearful'],
        "Date": str(datetime.datetime.now())
    }

    json_data = json.dumps(data_json)
    encrypted_data = AESCipher(bytes(key)).encrypt(json_data)
    print("hello face")
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db = client1.face
    DBFace = db[id]
    DBFace.insert_one({
        "encrypted_data": encrypted_data,
        "Date": data_json['Date']
    })

    f = open("timeLog.txt", 'w')
    f.close()

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

    print(encrypted_data)
    return Response({'data': data_json, 'face': result}, status=status.HTTP_200_OK)


# @api_view(['POST'])
# def gps(request):
#     if request.method == "POST":
#         print('gps 체크')
#         gps = request.POST['gps']
#         id = request.session.get("user_email")
#         uuid_name = uuid4().hex
#
#         data_json = {
#             "_id": uuid_name,
#             "gps": gps,
#             "Date": str(datetime.datetime.now())
#         }
#         json_data = json.dumps(data_json)
#
#         # Mongo 클라이언트 생성
#         client1 = mongo.MongoClient()
#         db = client1.gps
#         DBIp = db[id]
#
#         # 3개까지 기억
#         valid_gps_tf = False
#         result = DBIp.find().sort("Date", 1)
#         result = list(result)
#         if len(result) < 3:
#             valid_ip_tf = True
#             # 새로운 ip일 경우 등록
#             correct_tf = False
#             for data in result:
#                 if data['ip'] == ip:
#                     correct_tf = True
#             if not correct_tf:
#                 DBIp.insert_one(data_json)
#         else:
#             for data in result:
#                 if data['ip'] == ip:
#                     valid_ip_tf = True
#         if not valid_ip_tf:
#             db2 = client1.fail
#             dbfail = db2[id]
#             data = {
#                 "_id": uuid_name,
#                 "detection": "ip",
#                 "result": ip,
#                 "date": str(datetime.datetime.now())
#             }
#             dbfail.insert_one(data)
#
#         return Response({'validTF': valid_ip_tf}, status=status.HTTP_200_OK)

@api_view(['POST'])
def ip(request):
    if request.method == "POST":
        print('ip 체크')
        ip = request.POST['ip']
        id = request.session.get("user_email")
        uuid_name = uuid4().hex

        data_json = {
            "_id": uuid_name,
            "ip": ip,
            "Date": str(datetime.datetime.now())
        }
        json_data = json.dumps(data_json)

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.ip
        DBIp = db[id]

        # 3개까지 기억
        valid_ip_tf = False
        result = DBIp.find().sort("Date", 1)
        result = list(result)
        if len(result) < 3:
            valid_ip_tf = True
            # 새로운 ip일 경우 등록
            correct_tf = False
            for data in result:
                if data['ip'] == ip:
                    correct_tf = True
            if not correct_tf:
                DBIp.insert_one(data_json)
        else:
            for data in result:
                if data['ip'] == ip:
                    valid_ip_tf = True
        if not valid_ip_tf:
            db2 = client1.fail
            dbfail = db2[id]
            data = {
                "_id": uuid_name,
                "detection": "ip",
                "result": ip,
                "date": str(datetime.datetime.now())
            }
            dbfail.insert_one(data)

        return Response({'validTF': valid_ip_tf}, status=status.HTTP_200_OK)

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

    if request.method == "PATCH" and adminEmail == request.session.get("user_email"):
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

    if request.method == "PATCH" and adminEmail == request.session.get("user_email"):
        email = request.data['email']
        settingNum = request.data['settingNum']
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=email)
        encryptionAlgorithm.choice = settingNum
        encryptionAlgorithm.save()
        return Response('ok', status=status.HTTP_200_OK)