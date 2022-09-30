import base64
import hashlib
import hmac
import time
import json
from random import randint
import random

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

# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.utils import json

from emotionSys.models import User, AuthSms, Auth_Category, AuthEmail, Emotion, EncryptionAlgorithm, ChoiceCheck  # , User_Security, Security
from my_settings import EMAIL

# 암복호화 관련
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

def main(request):

    request.method == 'GET'
    user_email = request.session.get('user')
    print(user_email)

    return render(request, 'index.html', {'field': user_email})

def main2(request):
    request.method == 'GET'
    user_email = request.session.get('user')
    print(user_email)
    return render(request, 'index2.html', {'field': user_email})



@csrf_exempt
def dashBoard(request):
    request.method == 'GET'
    user = request.session.get('user')

    gps = request.GET.get('gps')
    device = request.GET.get('device')
    client1 = mongo.MongoClient()
    dbs = client1.log
    DBLog = dbs["admin"]
    data = {"log": "dashboard", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}
    try:
        user = User.objects.get(email=user)

        if user.type == 1:
            auth_category = Auth_Category.objects.all()

            print(auth_category)
            return render(request, 'dash.html', {"user_data": user, "auth_category": auth_category})

        # else :

        # user_security = User_Security.objects.select_related("security").filter(user=user)

        # return render(request, 'dash.html', {"user_data": user, "user_auth": user_auth})

        # user_security = User_Security.objects.select_related("security").filter(user=user)
        # print(user_security.values())
        # print(user_security)
    except User.DoesNotExist:
        return render(request, 'index.html', {'error': 'not connect'})

    # return render(request, 'dash.html', {"data": user_security, "user_data": user})
    return render(request, 'dash.html', {"user_data": user})


def emotion(request):
    request.method == 'GET'
    user_email = request.session.get('user_email')

    return render(request, 'check.html', {'field': user_email})


def emotion_result(request):
    request.method == 'GET'

    return render(request, 'result.html')


def emotion_face(request):
    request.method == 'GET'

    return render(request, 'face.html')


def re_auth(request):
    request.method == 'GET'

    # user = request.session.get('user')
    try:
        # user = User.objects.get(email=user)

        auth_category = Auth_Category.objects.all()

        print(auth_category)
        return render(request, 're_check.html', {"auth_category": auth_category})

    except User.DoesNotExist:
        return render(request, 're_check.html', {'error': 'not connect'})


def signOut(request):
    if request.session.get('user'):
        del (request.session['user'])
    return redirect('main')


def phone(request):
    if request.method == 'GET':
        return render(request, 'phonecheck.html')


@csrf_exempt
def signIn(request):
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']
        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'not connect'})

        request.session['userName'] = user.name
        request.session['type'] = user.type
        request.session['user_email'] = user.email

        return render(request, 'index.html', {'field': user_email, 'username': request.session.get('userName')})


def user_log(request):
    if request.method == 'GET':
        request.method == 'GET'
        user = request.session.get('user')

        # Mongo 클라이언트 생성
        client1 = mongo.MongoClient()

        # 호스트와 포트를 지정
        client2 = mongo.MongoClient('localhost', 27017)

        # 데이터베이스를 생성 혹은 지정
        # db = client1.face
        # db1 = client1.voice
        dbs = client1.emotion_log

        id = request.session.get("user")

        # DBFace = db[id]
        # DBVoice = db1[id]
        DBEmotion = dbs[id]

        result = DBEmotion.find().sort("date", -1)
        return render(request, 'user_log.html', {'data': result})


def email_sign(request):
    if request.method == 'GET':
        current_site = get_current_site(request)
        print(current_site)

        domain = current_site.domain
        mail_title = "이메일 2차 인증을 완료해주세요"
        message_data = "https://192.168.64.94:8000/users/check"
        email = EmailMessage(mail_title, message_data, to=['20161658@g.dongseo.ac.kr'])

        email.send()

        return JsonResponse({"message": "SUCCESS"}, status=200)


def activate(request):
    if request.method == 'GET':
        return redirect(EMAIL['REDIRECT_PAGE'])


def check_sms(request):
    if request.method == 'POST':
        user_email = request.session.get('user')
        input_data = request.POST['number']

        user = User.objects.get(email=user_email)
        auth = AuthSms.objects.get(auth_phone=user.phone)

        if int(input_data) == int(auth.auth_number):
            return render(request, 'approval.html')

        else:
            return render(request, 're_check.html')


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


class AuthSmsView(View):

    # def send_sms(self, auth_phone, auth_number):
    #
    #     messages = {"to": str(auth_phone)}
    #
    #     data = {
    #         'type': 'SMS',
    #         'contentType': 'COMM',
    #         'countryCode': '82',
    #         'from': "01093964847",
    #         'content': "인증번호 : " + str(auth_number),
    #         'messages': [messages]
    #     }
    #     body2 = json.dumps(data)
    #
    #     headers = {
    #         'Content-Type': 'application/json; charset=utf-8',
    #         'x-ncp-apigw-timestamp': timestamp,
    #         'x-ncp-iam-access-key': access_key,
    #         'x-ncp-apigw-signature-v2': make_signature(),
    #     }
    #
    #     res = requests.post(apiUrl, headers=headers, data=body2)

    def get(self, request):
        try:
            user_email = request.session.get('user')
            user = User.objects.get(email=user_email)

            # input_data = json.loads(request.body)
            # input_phone_number = input_data['auth_phone']
            input_phone_number = user.phone
            created_auth_number = randint(1000, 10000)
            exist_phone_number = AuthSms.objects.get(auth_phone=input_phone_number)
            exist_phone_number.auth_number = created_auth_number
            exist_phone_number.save()
            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'authSms.html')

        except AuthSms.DoesNotExist:
            AuthSms.objects.create(
                auth_phone=input_phone_number,
                auth_number=created_auth_number
            ).save()

            self.send_sms(auth_phone=input_phone_number, auth_number=created_auth_number)

            return render(request, 'authSms.html')


def v2_main(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')
        gps = request.GET.get('gps')
        device = request.GET.get('device')
        client1 = mongo.MongoClient()
        dbs = client1.log
        DBLog = dbs["admin"]
        data = {"log": "main", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}

        if user_email is None:
            return render(request, 'index.html')
        else:
            encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

            if encryptionAlgorithm == 1:  # 대칭키
                symmetrical_key = request.session.get('symmetrical_key')
                return render(request, 'index.html',
                              {'encryption_algorithm': encryptionAlgorithm,
                               'symmetrical_key': symmetrical_key,
                               'username': request.session.get('userName'),
                               'type': request.session.get('type')
                               })
            elif encryptionAlgorithm == 2:  # 비대칭키
                key = RSA.importKey(request.session.get('receive_key'))
                # 퍼블릭 키 얻기
                public_key = key.public_key()
                # 퍼블릭 키 문자열로 변환하기
                public_key_string = public_key.exportKey('PEM').decode("ascii")

                # 서버가 데이터를 보낼 때 사용할 키
                key = RSA.importKey(request.session.get('send_key'))
                # 프라이빗 키 문자열로 변환하기
                private_key_string = key.exportKey('PEM').decode("ascii")

                return render(request, 'index.html',
                              {'encryption_algorithm': encryptionAlgorithm,
                               'public_key': public_key_string,
                               'private_key': private_key_string,
                               'username': request.session.get('userName'),
                               'type': request.session.get('type')
                               })

def v2_userManager(request):
    request.method == 'GET'
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    dbs = client1.log
    #로그 기록 찍기
    id = request.session.get("user_email")
    DBEmotion = dbs[id]
    gps = request.GET.get('gps')
    device = request.GET.get('device')
    data = {"log": "userManager", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}
    DBEmotion.insert_one(data)

    # 유저가 없는 경우 메인 화면으로 보냄
    try:
        users = User.objects.all()
    except User.DoesNotExist:
        return render(request, 'index.html', {'error': 'No signIn'})

    # 첫 번째 유저의 추가 인증 수단이 설정되지 않은 경우 메인 화면으로 보냄 (검토 필요)
    try:
        choiceCheck = ChoiceCheck.objects.get(email=users[0].email)
    except ChoiceCheck.DoesNotExist:
        return render(request, 'index.html', {'error': 'No signIn'})

    # 첫 번째 유저의 암호화 알고리즘이 설정되지 않은 경우 메인 화면으로 보냄 (검토 필요)
    try:
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=users[0].email)
    except EncryptionAlgorithm.DoesNotExist:

        return render(request, 'index.html', {'error': 'No signIn'})



    return render(request, 'userManager.html', {'username': request.session.get('userName'), 'type': request.session.get('type'),"users":users,"initialization":[choiceCheck.choice,encryptionAlgorithm.choice]})



def v2_userlog(request):
    request.method == 'GET'
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()

    # 데이터베이스를 생성 혹은 지정
    dbs = client1.log
    id = request.session.get("user_email")
    #로그 기록 찍기
    gps = request.GET.get('gps')
    device = request.GET.get('device')
    client1 = mongo.MongoClient()
    dbs = client1.log
    DBLog = dbs[id]
    data = {"log": "userLog", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}

    DBEmotion = dbs[id]

    result = DBEmotion.find().sort("date", -1);
    DBEmotion.insert_one(data);
    return render(request, 'userlog.html', {'data': result, 'username': request.session.get('userName'), 'type': request.session.get('type')})

def v2_facelog(request):
    request.method == 'GET'

    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    # 데이터베이스를 생성 혹은 지정
    db = client1.face
    id = request.session.get("user_email")
    # 콜렉션을 지정
    DBFace = db[id]

    result = DBFace.find().sort("Date", -1)
    ### 대칭키 복호화의 경우 ###
    # #리스트로 변환
    # result = list(result)
    #
    # # rsult리스트의 데이터들을 복호화 함
    # for index, item in enumerate(result):
    #     encrypted_data = item['encrypted_data']
    #     decrypted_data = AESCipher(bytes(key)).decrypt(encrypted_data)
    #     decrypted_data.decode('utf-8')
    #     decrypted_data = json.loads(decrypted_data)
    #     result[index] = {
    #         "_id": item['_id'],
    #         "neutral": decrypted_data['neutral'],
    #         "happy": decrypted_data['happy'],
    #         "angry": decrypted_data['angry'],
    #         "sad": decrypted_data['sad'],
    #         "fearful": decrypted_data['fearful'],
    #         "Date": item['Date']
    #     }
    ######
    #로그 기록 찍기
    gps = request.GET.get('gps')
    device = request.GET.get('device')
    client1 = mongo.MongoClient()
    dbs = client1.log
    dbslog = dbs[id];
    data = {"log": "faceLog", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}
    dbslog.insert_one(data)
    return render(request, 'facelog.html', {'data': result, 'username': request.session.get('userName'), 'data2': result, 'type': request.session.get('type')})

def v2_voicelog(request):
    request.method == 'GET'
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db1 = client1.voice
    id = request.session.get("user_email")

    DBVoice = db1[id]

    result = DBVoice.find().sort("date", -1)
    ### 대칭키 복호화의 경우 ###
    # #리스트로 변환
    # result = list(result)
    #
    # # rsult리스트의 데이터들을 복호화 함
    # for index, item in enumerate(result):
    #     encrypted_data = item['encrypted_data']
    #     decrypted_data = AESCipher(bytes(key)).decrypt(encrypted_data)
    #     decrypted_data.decode('utf-8')
    #     decrypted_data = json.loads(decrypted_data)
    #
    #     result[index] = {
    #         '_id': item['_id'],
    #         'positive': decrypted_data['positive'],
    #         'negative': decrypted_data['negative'],
    #         'date': item['date']
    #     }

    client2 = mongo.MongoClient()
    db2 = client2.voice_count

    DBVoice_Cnt = db2[id]

    result_cnt = DBVoice_Cnt.find_one({'_id': id})

    print(result_cnt)
    #로그 기록 찍기
    gps = request.GET.get('gps')
    device = request.GET.get('device')
    client1 = mongo.MongoClient()
    dbs = client1.log
    DBLog = dbs[id]
    data = {"log": "voiceLog", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}
    DBLog.insert_one(data)
    return render(request, 'voicelog.html', {'data': result, 'username': request.session.get('userName'), 'data_cnt': result_cnt, 'type': request.session.get('type')})


def v2_faillog(request):
    request.method == 'GET'
    # Mongo 클라이언트 생성
    client1 = mongo.MongoClient()
    db1 = client1.fail
    id = request.session.get("user_email")

    DBfail = db1[id]

    result = DBfail.find().sort("date", -1)

    cnt = {
        "face": DBfail.find({'detection': 'face'}).count,
        "voice": DBfail.find({'detection': 'voice'}).count
    }
    #로그 기록 찍기
    gps = request.GET.get('gps')
    device = request.GET.get('device')
    client1 = mongo.MongoClient()
    dbs = client1.log
    DBLog = dbs[id]
    data = {"log": "failLog", "date": str(datetime.datetime.now()), "GPS": gps, "device": device}
    DBLog.insert_one(data)
    return render(request, 'faillog.html', {'data': result, 'username': request.session.get('userName'), 'cnt': cnt,'type': request.session.get('type')})


def v2_signIn(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':

        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']

        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
            return render(request, 'index.html', {'error': 'No signIn'})

        request.session['user_email'] = user.email
        request.session['type'] = user.type
        request.session['userName'] = user.name
        # 로그 기록 찍기
        # gps = request.GET['gps']
        # device = request.GET['device']
        # client1 = mongo.MongoClient()
        # dbs = client1.log
        # DBLog = dbs["admin"]
        # data = {"log": "signin", "date": datetime.datetime.now(), "GPS": gps, "device": device}
    #
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:  # 대칭키
            alphabet_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            random_list = random.sample(alphabet_string, 16)
            symmetrical_key = ''.join(random_list)
            request.session['symmetrical_key'] = symmetrical_key

            return render(request, 'index.html',
                          {'encryption_algorithm': encryptionAlgorithm,
                           'symmetrical_key': symmetrical_key,
                           'username': request.session.get('userName'),
                           'type': request.session.get('type')
                           })
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

            return render(request, 'index.html',
                            {'encryption_algorithm': encryptionAlgorithm,
                            'public_key': public_key_string,
                            'private_key': private_key_string,
                            'username': request.session.get('userName'),
                            'type': request.session.get('type')
                            })
    #

def v2_signOut(request):
    request.session.clear()
    return redirect('/v2/main')

def v2_signUp(request):
    if request.method == 'GET':
        return render(request, 'register.html')


    elif request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']

        User.objects.create(
            email=user_email,
            password=user_pw
        ).save()

        return render(request, 'index.html')


def v2_fail(request):
    if request.method == 'GET':
        # auth_category = Auth_Category.objects.all()

        # 로그 기록 찍기
        # gps = request.GET['gps']
        # device = request.GET['device']
        # client1 = mongo.MongoClient()
        # dbs = client1.log
        # DBLog = dbs["admin"]
        # data = {"log": "fail", "date": datetime.datetime.now(), "GPS": gps, "device": device}

        return render(request, 'check.html', {'username': request.session.get('userName'), 'type': request.session.get('type')})

def v2_emotionlog(request):
    client1 = mongo.MongoClient()
    emotion_db = client1.emotion
    emotion_collection = emotion_db.emotion
    result = emotion_collection.find({})
    user_email = request.session.get('user_email')

    return render(request, 'userEmotion.html',
                  {'result': result,
                   'user': user_email
                   })

def v2_emotionLogDetail(request,method=''):
    client1 = mongo.MongoClient()
    emotion_db = client1.emotion  # database 선택
    emotion_collection = emotion_db.emotion  # collection 선택
    result = emotion_collection.find({})  # document 모두 조회
    user_email = request.session.get('user_email')

    list = []
    for emotion in result:
        face = emotion['face']
        voice = emotion['voice']
        brain = emotion['brain']
        id = emotion['id']
        user = emotion['user']
        create_at = emotion['createAt']

        if method == 'Default':
            list.append({'id': id,
                         'face': face,
                         'voice': voice,
                         'brain': brain,
                         'user': user,
                         'createAt': create_at,
                         'result': emotionDetailDefault(face, voice, brain)
                         })
        if method == 'Fuzzy':
            list.append({'id': id,
                         'face': face,
                         'voice': voice,
                         'brain': brain,
                         'user': user,
                         'createAt': create_at,
                         'result': emotionDetailFuzzy(face, voice, brain)
                         })
        if method == 'Maut':
            list.append({'id': id,
                         'face': face,
                         'voice': voice,
                         'brain': brain,
                         'user': user,
                         'createAt': create_at,
                         'result': emotionDetailMaut(face, voice, brain)
                         })
        if method == 'Graph':
            list.append({'id': id,
                         'face': face,
                         'voice': voice,
                         'brain': brain,
                         'user': user,
                         'createAt': create_at,
                         'result': False
                         })

    return render(request, 'userEmotion'+method+'.html',
                  {'result': list,
                   'data': request.session.get('userName'),
                   'user': user_email,
                   'field': user_email,
                   'username': request.session.get('userName'),
                   'type': request.session.get('type')
                   })

def emotionDetailDefault(face,voice,brain):
    cnt = 0;
    if face >= 0.5:
        cnt = cnt + 1
    if voice >= 0.5:
        cnt = cnt + 1
    if brain >= 0.5:
        cnt = cnt + 1
    if cnt > 2:
        return True
    else:
        return False

def emotionDetailFuzzy(face,voice,brain):
    if face >= 0.7 and voice >= 0.7 and brain >= 0.7:
        return True
    else:
        return False

def emotionDetailMaut(face,voice,brain):
    if face * 0.3 + voice * 0.3 + brain * 0.4 > 0.8:
        return True
    else:
        return False

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

def v2_questionCheck(request):
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
            return render(request, 'index.html',
                          {'username': request.session.get('userName'), 'type': request.session.get('type')})

        else:
            print('fail')
            return render(request, 'check.html')



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

# def v2_locateCheck(request):
#     if request.method == 'GET':
#
#         if(false)
#             return render(request, 'check.html')
#
#         else
#             return render(request, 'index.html')


def v2_dashBoard(request):
    if request.method == 'GET':

        user_email = request.session.get('user_email')

        user = User.objects.get(email=user_email)

        if user.type == 1:
            auth_category = Auth_Category.objects.all()

            client1 = mongo.MongoClient()
            client2 = mongo.MongoClient('localhost', 27017)

            dbs = client1.emotion_log

            id = request.session.get("user_email")

            DBEmotion = dbs[id]

            # 로그 기록 찍기
            # gps = request.GET['gps']
            # device = request.GET['device']
            # client1 = mongo.MongoClient()
            # dbs = client1.log
            # DBLog = dbs["admin"]
            # data = {"log": "userlog", "date": datetime.datetime.now(), "GPS": gps, "device": device}
            result = DBEmotion.find()
            return render(request, 'profile.html', {"auth_category": auth_category,
                                                    "data": result, 'type': request.session.get('type')})

        else:
            return render(request, 'profile.html')
