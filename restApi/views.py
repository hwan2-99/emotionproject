import json
from builtins import str

import uuid as uuid
from django.shortcuts import render

# Create your views here.
import datetime
import numpy as np
import base64
import pymongo as mongo
import json
from datetime import date
#from datetime import datetime
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

# 암복호화 관련
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

# 로그 파일 생성 작업용
import time
import uuid

adminEmail = 'admin@gmail.com'

key = [0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72, 0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
        0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72, 0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F]

def symmetric_decrypt(enc, symmetrical_key):
    enc = base64.b64decode(enc)
    cipher = AES.new(symmetrical_key.encode('utf-8'), AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16)

@csrf_exempt
@api_view(['GET', 'POST'])
def voice(request):
    # today = date.today()
    #encrypt_startTime = datetime.now()
    if request.method == "POST":
        # nchannels = 1
        # sampwidth = 1
        # framerate = 8000
        # nframes = 1
        #
        # name = 'output.wav'
        # audio = wave.open(name, 'wb')
        # audio.setnchannels(nchannels)
        # audio.setsampwidth(sampwidth)
        # audio.setframerate(framerate)
        # audio.setnframes(nframes)
        # blob = open("original.wav").read()  # such as `blob.read()`
        # audio.writeframes(blob)

        # 음성 서버에 저장하는 작업
        #audio_file = request.FILES.get('audio_data', None)
        encrypted = request.POST['encrypted_audio_data']
        if EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 1:
            symmetrical_key = request.session.get('symmetrical_key')
            print('대칭키', symmetrical_key)
        elif EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 2:
            encrypted_key = request.POST['encrypted_key']
            key = RSA.importKey(request.session.get('receive_key'))
            decryptor = PKCS1_v1_5.new(key)
            # 대칭키 복호화
            ciphertext = base64.b64decode(encrypted_key.encode('ascii'))
            plaintext = decryptor.decrypt(ciphertext, b'DECRYPTION FAILED')
            decrypted_key = plaintext.decode('utf8')
            print('복호화 한 대칭키', decrypted_key)
            symmetrical_key = decrypted_key

        # 파일 복호화 (대칭 키)
        decrypted = symmetric_decrypt(bytes(encrypted,'utf-8'), symmetrical_key)
        encode_string = decrypted.decode("utf-8", "ignore")
        decode_byte = base64.b64decode(encode_string)
        # 로그 파일 생성
        index = uuid.uuid4()
        userEmail = request.session.get('user_email')
        dataType = 'voice_data'
        startTime = int(request.POST['startTime'])  # 시작 시간
        endTime = int(time.time()*1000)  # 끝 시간
        timeGap = endTime-startTime
        if EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 1:
            encryption_algorithm = 'symmetry'
        elif EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 2:
            encryption_algorithm = 'asymmetry'
        else:
            raise Exception("unvalid encryption algorithm")
        with open('voiceLog.txt', 'a') as f:
            f.write(str(index)+"|"+str(userEmail)+"|"+str(dataType)+"|"+str(startTime)+"|"+str(endTime)+"|"+str(timeGap)+"|"+str(encryption_algorithm)+"\n")
        # 복호화 wav 파일 저장
        with open("temp.wav", "wb") as wav_file:
            wav_file.write(decode_byte)
        # 복호화 wav 파일 읽기
        #obj = wave.open(audio_file, 'r')
        wav_file = open("temp.wav", "rb")
        wf = wave.open(wav_file, 'r')
        # test.wav 생성
        audio = wave.open('voiceEmotion/test.wav', 'wb')
        audio.setnchannels(wf.getnchannels())
        audio.setnframes(wf.getnframes())
        audio.setsampwidth(wf.getsampwidth())
        audio.setframerate(wf.getframerate())
        #blob = audio_file.read()  # bytes타입
        blob = decode_byte
        audio.writeframes(blob)

        #
        # with open('test.txt', 'w') as f:
        #     f.write('원본' + str(blob) + '\n')
        #

        # 내용물 확인 테스트
        with open('test22.txt', 'w') as f:
            f.write('흉내' + str(decode_byte) + '\n')

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

        # # json 데이터 직렬화
        # json_data = json.dumps(data_json)
        # # 암호화
        # encrypted_data = AESCipher(bytes(key)).encrypt(json_data)

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

        #encrypt_endTime = datetime.now()

        #encrypt_Time = encrypt_endTime - encrypt_startTime

        return Response({'data': data_json}, status=status.HTTP_200_OK)

@api_view(['GET','POST'])
def face(request):
    #복호화
    # key = RSA.import_key(request.session.get('receive_key'))
    # encryptedText = request.POST['encryptedText']
    # decryptor = PKCS1_OAEP.new(key)
    # decrypted = decryptor.decrypt(ast.literal_eval(str(encryptedText)))
    # print('복호화!!', str(decrypted))

    faceURL = request.POST['faceURL']
    neutral = request.POST['neutral']
    happy = request.POST['happy']
    angry = request.POST['angry']
    sad = request.POST['sad']
    fearful = request.POST['fearful']
    startTime = request.POST['startTime']

    if EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 1:
        symmetrical_key = request.session.get('symmetrical_key')
        print('대칭키', symmetrical_key)
    elif EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 2:
        encrypted_key = request.POST['encrypted_key']
        key = RSA.importKey(request.session.get('receive_key'))
        decryptor = PKCS1_v1_5.new(key)
        # 대칭키 복호화
        ciphertext = base64.b64decode(encrypted_key.encode('ascii'))
        plaintext = decryptor.decrypt(ciphertext, b'DECRYPTION FAILED')
        decrypted_key = plaintext.decode('utf8')
        symmetrical_key = decrypted_key
        print('복호화 한 대칭키', symmetrical_key)

    # 데이터 복호화 (대칭 키)
    faceURL = symmetric_decrypt(bytes(faceURL, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    neutral = symmetric_decrypt(bytes(neutral, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    happy = symmetric_decrypt(bytes(happy, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    angry = symmetric_decrypt(bytes(angry, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    sad = symmetric_decrypt(bytes(sad, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    fearful = symmetric_decrypt(bytes(fearful, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")
    startTime = symmetric_decrypt(bytes(startTime, 'utf-8'), symmetrical_key).decode("utf-8", "ignore")

    # 로그 파일 생성
    index = uuid.uuid4()
    userEmail = request.session.get('user_email')
    dataType = 'face_data'
    startTime = int(startTime)  # 시작 시간
    endTime = int(time.time() * 1000)  # 끝 시간
    timeGap = endTime - startTime
    if EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 1:
        encryption_algorithm = 'symmetry'
    elif EncryptionAlgorithm.objects.get(email=request.session.get("user_email")).choice == 2:
        encryption_algorithm = 'asymmetry'
    else:
        raise Exception("unvalid encryption algorithm")
    with open('faceLog.txt', 'a') as f:
        f.write(str(index) + "|" + str(userEmail) + "|" + str(dataType) + "|" + str(startTime) + "|" + str(
            endTime) + "|" + str(timeGap) + "|" + str(encryption_algorithm) + "\n")

    image = faceURL.split(',')[1]
    decoded_data = base64.b64decode(image)
    np_data = np.fromstring(decoded_data, np.uint8)
    id = request.session.get("user_email")
    result = myface(np_data,id)

    uuid_name = uuid4().hex
    data_json = {
        "_id": uuid_name,
        "neutral": neutral,
        "happy": happy,
        "angry": angry,
        "sad": sad,
        "fearful": fearful,
        "Date": str(datetime.datetime.now())
    }

    json_data = json.dumps(data_json)
    #encrypted_data = AESCipher(bytes(key)).encrypt(json_data)
    print("hello face")
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db = client1.face
    DBFace = db[id]
    DBFace.insert_one(data_json)

    f = open("timeLog.txt", 'w')
    f.close()

    if float(fearful) >= 0.2:
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

    return Response({'data': data_json, 'face': result}, status=status.HTTP_200_OK)


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