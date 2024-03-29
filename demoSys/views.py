import base64
import hashlib
import hmac

import json
from random import randint
import random
import socket

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

# Create your views here.
from requests import Response
from rest_framework import status
from rest_framework.utils import json

# sqlite3 모델들
from emotionSys.models import User, AuthSms, Auth_Category, AuthEmail, Emotion, EncryptionAlgorithm, ChoiceCheck  # , User_Security, Security
from my_settings import EMAIL

# 암복호화 관련
from Crypto.PublicKey import RSA
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

from uuid import uuid4

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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
                       }

            demoLog.insert_one(userLog)

            return render(request, 'demo_info.html',
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

            act = '사용자 로그인 시도(성공)'
            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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

        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:

            userLog = {'userId': user_email,
                       'date': now.strftime('%Y-%m-%d %H:%M:%S'),
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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
                       'gps': '-',
                       'ip': socket.gethostbyname(socket.gethostname()),
                       'action': act,
                       'warningYN': '-'
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

def v2_demoEmailCheck(request):
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
                          'demoEmailCheck.html',
                          {'userEmail': request.session.get('user_email')})


def v2_demo_logOut(request):
    act = '로그아웃'
    now = time
    client1 = mongo.MongoClient()
    dbs = client1.securiry
    demoLog = dbs.demosecurity

    user_email = request.session.get('user_email')
    userLog = {'userId': user_email,
               'date': now.strftime('%Y-%m-%d %H:%M:%S'),
               'gps': '-',
               'ip': socket.gethostbyname(socket.gethostname()),
               'action': act,
               'warningYN': '-'
               }

    demoLog.insert_one(userLog)

    request.session.clear()

    return redirect('/v2/demo')

