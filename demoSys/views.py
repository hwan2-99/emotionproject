import base64
import hashlib
import hmac

import json
import uuid
import wave
from random import randint
import random
import socket
import numpy as np

import datetime
from datetime import date
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import pymongo as mongo
import time
from uuid import uuid4
# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.utils import json

# sqlite3 모델들
from emotionSys.models import User, AuthSms, Auth_Category, AuthEmail, Emotion, EncryptionAlgorithm, ChoiceCheck  # , User_Security, Security
from faceEmotion.face_Recognition import myface
from my_settings import EMAIL

# 암복호화 관련
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

from uuid import uuid4

from voiceEmotion.main import emotionCheck


def v2_demo_login(request):
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry
    demoLog = dbs.demosecurity

    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']

        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
            act = '사용자 로그인 시도(실패)'
            return render(request, 'demo.html', {'error': 'No signIn'})

        request.session['user_email'] = user.email
        request.session['type'] = user.type
        request.session['userName'] = user.name



        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:  # 대칭키
            alphabet_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            random_list = random.sample(alphabet_string, 16)
            symmetrical_key = ''.join(random_list)
            request.session['symmetrical_key'] = symmetrical_key

            act = '사용자 로그인 시도(성공)'
            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)

            return redirect('/v2/demo_info')

            # return render(request, 'demo_info.html',
            #               {'encryption_algorithm': encryptionAlgorithm,
            #                'symmetrical_key': symmetrical_key,
            #                'username': request.session.get('userName'),
            #                'type': request.session.get('type')
            #                })
        elif encryptionAlgorithm == 2:  # 비대칭키
            # 서버가 데이터를 받을 때 사용할 키 -> 세션에 저장
            key = RSA.generate(3072)
            request.session['receive_key'] = str(key.exportKey('PEM').decode("ascii"))
            # 퍼블릭 키 얻기
            public_key = key.public_key()
            # 퍼블릭 키 문자열로 변환하기
            public_key_string = public_key.exportKey('PEM').decode("ascii")

            # 서버가 데이터를 보낼 때 사용할 키 -> 세션에 저장
            key = RSA.generate(3072)
            request.session['send_key'] = str(key.exportKey('PEM').decode("ascii"))
            # 프라이빗 키 문자열로 변환하기
            private_key_string = key.exportKey('PEM').decode("ascii")

            act = '사용자 로그인 시도(성공)'
            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            return render(request, 'demo_info.html',
                            {'encryption_algorithm': encryptionAlgorithm,
                            'public_key': public_key_string,
                            'private_key': private_key_string,
                            'username': request.session.get('userName'),
                            'type': request.session.get('type')
                            })

def v2_demo(request):
    if request.method == 'GET':
        return render(request, 'demo.html', {
        })

def v2_demo_info(request):

    act = '사용자 상황정보 수집 및 조회 클릭'
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry     #데이터 베이스 선택
    demoLog = dbs.demosecurity     # 컬렉션 선택
    result = demoLog.find({})
    list = []

    for log in result:
        userId = log['userId']
        date = log['date']
        ip = log['ip']
        action = log['action']

        list.append({'id': id,
                     'userId': userId,
                     'date': date,
                     'ip': ip,
                     'action': action
                     })


    user_email = request.session.get('user_email')

    if request.method == 'GET':

        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice


        if encryptionAlgorithm == 1:

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)
            return render(request, 'demo_info.html', {
                'result': list,
                'encryption_algorithm': encryptionAlgorithm,
                'symmetrical_key': request.session.get('symmetrical_key'),
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

        elif encryptionAlgorithm == 2:
            key = RSA.importKey(request.session.get('receive_key'))
            public_key = key.public_key()
            public_key_string = public_key.exportKey('PEM').decode("ascii")

            key = RSA.importKey(request.session.get('send_key'))
            private_key_string = key.exportKey('PEM').decode("ascii")

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)

            return render(request, 'demo_info.html', {
                'result': list,
                'encryption_algorithm': encryptionAlgorithm,
                'public_key': public_key_string,
                'private_key': private_key_string,
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

def v2_demo_certification(request):
    act = '사용자 인증 서비스 클릭'
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry
    demoLog = dbs.demosecurity
    user_email = request.session.get('user_email')

    if request.method == 'GET':


        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:
            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)
            return render(request, 'demo_certification.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'symmetrical_key': request.session.get('symmetrical_key'),
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })
        elif encryptionAlgorithm == 2:
            key = RSA.importKey(request.session.get('receive_key'))
            public_key = key.public_key()
            public_key_string = public_key.exportKey('PEM').decode("ascii")

            key = RSA.importKey(request.session.get('send_key'))
            private_key_string = key.exportKey('PEM').decode("ascii")

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)

            return render(request, 'demo_certification.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'public_key': public_key_string,
                'private_key': private_key_string,
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

def v2_demo_encryption(request):
    act = '데이터 암복호화 서비스 클릭'
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry
    demoLog = dbs.demosecurity
    user_email = request.session.get('user_email')

    if request.method == 'GET':
        return render(request, 'demo_encryption.html', {
            'symmetrical_key': "bo7ErxS1avMOtIWR",
            'username': request.session.get('userName'),
            'type': request.session.get('type'),
        })

        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)
            return render(request, 'demo_encryption.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'symmetrical_key': request.session.get('symmetrical_key'),
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })
        elif encryptionAlgorithm == 2:

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act
                       }

            demoLog.insert_one(userLog)
            key = RSA.importKey(request.session.get('receive_key'))
            public_key = key.public_key()
            public_key_string = public_key.exportKey('PEM').decode("ascii")

            key = RSA.importKey(request.session.get('send_key'))
            private_key_string = key.exportKey('PEM').decode("ascii")

            return render(request, 'demo_encryption.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'public_key': public_key_string,
                'private_key': private_key_string,
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

def v2_demo_logOut(request):
    act = '로그아웃'
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry
    demoLog = dbs.demosecurity

    user_email = request.session.get('user_email')
    userLog = {'userId': user_email,
               'date': now.strftime('%Y-%m-%d %H:%M:%S'),
               'ip': socket.gethostbyname(socket.gethostname()),
               'action': act
               }

    demoLog.insert_one(userLog)

    request.session.clear()

    return redirect('/v2/demo')

def v2_emailCheck(request):
    if request.method == 'GET':

        try:
            user_email = request.session.get('user_email')
            user = User.objects.get(email=user_email)

            print(user_email)
            if user is None:
                print('not')
                return render(request, 'check.html')

            user_email = user.email
            created_auth_number = randint(1000, 10000)
            auth_email = AuthEmail.objects.get(auth_email=user_email)
            auth_email.auth_number = created_auth_number
            auth_email.save()

            mail_title = "[데모 시스템] 이메일 2차 인증"
            message_data = "OTP 인증을 위해 다음 번호를 입력해주세요 : " + str(created_auth_number)
            email = EmailMessage(mail_title, message_data, to=[user_email])
            email.send()

            return render(request, 'emailCheck.html', {'data': user_email})

        except AuthEmail.DoesNotExist:
            created_auth_number = randint(1000, 10000)
            AuthEmail.objects.create(
                auth_email=user_email,
                auth_number=created_auth_number
            ).save()

            mail_title = "[데모 시스템] 이메일 2차 인증"
            message_data = "OTP 인증을 위해 다음 번호를 입력해주세요 : " + str(created_auth_number)
            email = EmailMessage(mail_title, message_data, to=[user_email])
            email.send()

            return render(request, 'emailCheck.html', {'data': user_email})

    elif request.method == 'POST':
        user_email = request.session.get('user_email')
        input_data = request.POST['number']

        user = User.objects.get(email=user_email)
        email = AuthEmail.objects.get(auth_email=user.email)

        if int(input_data) == int(email.auth_number):
            print('collect')
            return render(request, 'index.html', {'username': request.session.get('userName'), 'type': request.session.get('type')})

        else:
            print('fail')
            return render(request, 'check.html')

def v2_patternCheck(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')

        gps = request.GET.get('gps')
        device = request.GET.get('device')
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs["admin"]
        data = {"log": "main", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}

        user = User.objects.get(email=user_email)

        if user_email is None:
            return render(request, 'index.html')
        else:

            return render(request,
                          'patternCheck.html',
                          {'username': request.session.get('userName'),
                           'type': request.session.get('type'),
                            'pattern' : user.pattern
                           })

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)

url = "https://sens.apigw.ntruss.com"
requestUrl1 = "/sms/v2/services/"
requestUrl2 = "/messages"
serviceId = "ncp:sms:kr:266490177325:dsu_emotion"
access_key = "QRqgBlLhOPVszA8iAyXJ"

uri = requestUrl1 + serviceId + requestUrl2
apiUrl = url + uri

def make_signature():
    secret_key = "X8bxpHlTti6oFR3dg7cND3WwqquCV5lIb7OGy1qT"
    secret_key = bytes(secret_key, 'UTF-8')
    method = "POST"
    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')

    key = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())

    return key

def v2_questionCheck(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')

        # gps = request.GET.get('gps')
        # device = request.GET.get('device')
        # client1 = mongo.MongoClient()
        # dbs = client1.log
        # DBLog = dbs["admin"]
        # data = {"log": "main", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}

        user = User.objects.get(email=user_email)

        if user_email is None:
            return render(request, 'index.html')
        else:
            return render(request, 'questionCheck.html', {
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
                'question': user.question})

    elif request.method == 'POST':
        user_email = request.session.get('user_email')
        input_data = request.POST['answer']

        user = User.objects.get(email=user_email)

        if str(input_data) == str(user.answer):
            print('correct')
            return redirect('./demo_certification')
        else:
            print('fail')
            return render(request, 'questionCheck.html', {
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
                'question': user.question})

class v2_phoneCheck(View):
    def send_sms(self, auth_phone, auth_number):

        messages = {"to": str(auth_phone)}

        data = {
            'type': 'SMS',
            'contentType': 'COMM',
            'countryCode': '82',
            'from': "01093964847",
            'content': "인증번호 : " + str(auth_number),
            'messages': [messages]
        }
        body2 = json.dumps(data)

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'x-ncp-apigw-timestamp': timestamp,
            'x-ncp-iam-access-key': access_key,
            'x-ncp-apigw-signature-v2': make_signature(),
        }

        res = requests.post(apiUrl, headers=headers, data=body2)

    def get(self, request):

        try:
            user_email = request.session.get('user_email')
            user = User.objects.get(email=user_email)

            if user is None:
                return render(request, 'check.html')

            # input_data = json.loads(request.body)
            # input_phone_number = input_data['auth_phone']
            input_phone_number = user.phone
            created_auth_number = randint(1000, 10000)
            exist_phone_number = AuthSms.objects.get(auth_phone=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()
            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'phoneCheck.html', {'data': user.phone})

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                auth_phone=input_phone_number,
                auth_number=created_auth_number
            ).save()

            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'phoneCheck.html', {'data': user.phone})


    def post(self, request):

        user_email = request.session.get('user_email')
        input_data = request.POST['number']

        user = User.objects.get(email=user_email)
        auth = AuthSms.objects.get(auth_phone=user.phone)

        if int(input_data) == int(auth.auth_number):
            print('collect')
            return render(request, 'index.html', {'username': request.session.get('userName'), 'type': request.session.get('type')})

        else:
            print('fail')
            return render(request, 'check.html')

def v2_demo_analyze(request):
    if request.method == 'GET':
        return render(request, 'demo_analyze.html')

@api_view(['GET','POST'])
def demo_face(request):

    now = time
    neutral = request.POST['neutral']
    happy = request.POST['happy']
    angry = request.POST['angry']
    sad = request.POST['sad']
    fearful = request.POST['fearful']

    image = request.POST['faceURL'].split(',')[1]
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
    print("hello face")
    user_email = request.session.get('user_email')
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db = client1.analyze    # 데이터 베이스 선택
    faceLog = db.faceanalyze    # 컬렉션 선택
    logResult =  faceLog.find({})
    list = []

    if float(fearful) >= 0.2:
        print("fearful Test ~~~~~~~~~~~~~~~~~~")
        note = '불안한 감정'
    else:
        note = '-'

    for log in logResult:
        timestamp = log['timestamp']
        analyzeInfo = log['analyzeInfo']
        note = log['note']

        list.append({'timestamp': timestamp,
                     'analyzeInfo': fearful,
                     'note': note,
        })

    userLog = {'userId': user_email,
               'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
               'analyzeInfo': fearful,
               'note': note,
               }
    faceLog.insert_one(userLog)

    return Response({'data': data_json, 'face': result}, status=status.HTTP_200_OK)

def v2_demo_analyze_face(request):
    if request.method == 'POST':

        now = time
        neutral = request.POST['neutral']
        happy = request.POST['happy']
        angry = request.POST['angry']
        sad = request.POST['sad']
        fearful = request.POST['fearful']

        image = request.POST['faceURL'].split(',')[1]
        decoded_data = base64.b64decode(image)
        np_data = np.fromstring(decoded_data, np.uint8)

        id = request.session.get("user_email")
        result = myface(np_data, id)
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
        print("hello face")
        user_email = request.session.get('user_email')
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.analyze  # 데이터 베이스 선택
        faceLog = db.faceanalyze  # 컬렉션 선택
        logResult = faceLog.find({})
        list = []

        if float(fearful) >= 0.00000250:
            print("fearful Test ~~~~~~~~~~~~~~~~~~")
            note = '불안한 감정'
        else:
            note = '-'

        for log in logResult:
            timestamp = log['timestamp']
            analyzeInfo = log['analyzeInfo']
            note = log['note']

            list.append({'timestamp': timestamp,
                         'analyzeInfo': fearful,
                         'note': note,
                         })

        userLog = {'userId': user_email,
                   'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                   'analyzeInfo': analyzeInfo,
                   'note': note,
                   }

        faceLog.insert_one(userLog)

        return render(request, 'demo_analyze_face.html', {
            'face': result
            })

def v2_demo_analyze_face(request):

    if request.method == 'GET':
        now = time
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.analyze  # 데이터 베이스 선택
        faceLog = db.faceanalyze  # 컬렉션 선택
        logResult = faceLog.find({})
        list = []
        user_email = request.session.get('user_email')
        for log in logResult:
            timestamp = log['timestamp']
            analyzeInfo = log['analyzeInfo']
            note = log['note']

            list.append({'timestamp': timestamp,
                         'analyzeInfo': analyzeInfo,
                         'note': note,
                         })

        userLog = {'userId': user_email,
                   'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                   'analyzeInfo': analyzeInfo,
                   'note': note,
                   }

        faceLog.insert_one(userLog)

        return render(request, 'demo_analyze_face.html',{
            'logResult':list
        })

@csrf_exempt
@api_view(['GET', 'POST'])
def demo_voice(request):
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

def v2_demo_analyze_voice(request):
    if request.method == 'POST':

        now = time
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

        json_data = json.dumps(data_json)
        user_email = request.session.get('user_email')

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.analyze  # 데이터 베이스 선택
        voiceLog = db.voiceanalyze  # 컬렉션 선택
        logResult = voiceLog.find({})
        list = []

        if voiceresult['fear'] >= 0.5:
            print("fearful Test ~~~~~~~~~~~~~~~~~~")
            note = '불안한 감정'
        else:
            note = '-'

        for log in logResult:
            timestamp = log['timestamp']
            analyzeInfo = log['analyzeInfo']
            note = log['note']

            list.append({'timestamp': timestamp,
                         'analyzeInfo': voiceresult,
                         'note': note,
                         })

        userLog = {'userId': user_email,
                   'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                   'analyzeInfo': analyzeInfo,
                   'note': note,
                   }

        voiceLog.insert_one(userLog)

        return render(request, 'demo_analyze_voice.html', {
            'voice': voiceresult
            })

def v2_demo_analyze_voice(request):

    if request.method == 'GET':
        now = time
        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()
        db = client1.analyze  # 데이터 베이스 선택
        voiceLog = db.voiceanalyze  # 컬렉션 선택
        logResult = voiceLog.find({})
        list = []
        user_email = request.session.get('user_email')
        for log in logResult:
            timestamp = log['timestamp']
            analyzeInfo = log['analyzeInfo']
            note = log['note']

            print(analyzeInfo)
            list.append({'timestamp': timestamp,
                         'analyzeInfo': analyzeInfo,
                         'note': note,
                         })

        userLog = {'userId': user_email,
                   'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                   'analyzeInfo': analyzeInfo,
                   'note': note,
                   }

        voiceLog.insert_one(userLog)

        return render(request, 'demo_analyze_voice.html',{
            'logResult':list
        })