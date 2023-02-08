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
    if request.method == 'POST':
        user_email = request.POST['user_email']
        user_pw = request.POST['user_pw']

        try:
            user = User.objects.get(email=user_email, password=user_pw)

        except User.DoesNotExist:
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
    if request.method == 'GET':
        user_email = request.session.get('user_email')
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:
            return render(request, 'demo_info.html', {
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

            return render(request, 'demo_info.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'public_key': public_key_string,
                'private_key': private_key_string,
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

def v2_demo_certification(request):
    if request.method == 'GET':
        user_email = request.session.get('user_email')
        encryptionAlgorithm = EncryptionAlgorithm.objects.get(email=user_email).choice

        if encryptionAlgorithm == 1:
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

            return render(request, 'demo_certification.html', {
                'encryption_algorithm': encryptionAlgorithm,
                'public_key': public_key_string,
                'private_key': private_key_string,
                'username': request.session.get('userName'),
                'type': request.session.get('type'),
            })

def v2_demo_encryption(request):
    if request.method == 'GET':

        key = RSA.importKey(request.session.get('receive_key'))
        public_key = key.public_key()
        public_key_string = public_key.exportKey('PEM').decode("ascii")

        key = RSA.importKey(request.session.get('send_key'))
        private_key_string = key.exportKey('PEM').decode("ascii")

        return render(request, 'demo_encryption.html', {
            'symmetrical_key': request.session.get('symmetrical_key'),
            'public_key': public_key_string,
            'private_key': private_key_string,
            'username': request.session.get('userName'),
            'type': request.session.get('type'),
        })
