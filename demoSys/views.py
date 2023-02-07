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

from uuid import uuid4

def v2_demo(request):
    request.method == 'GET'
    user_email = request.session.get('user')

    return render(request, 'demo.html', {'field': user_email})