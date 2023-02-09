from random import randint

import requests
from django.db import models

# Create your models here.

from django.db import models

class User(models.Model):
    email = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    type = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pattern = models.IntegerField()
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)

    class Meta:
        db_table = "user"

class EncryptionAlgorithm(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=200)
    choice = models.IntegerField()

    class Meta:
        db_table = "encryption_algorithm"

class ChoiceCheck(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=200)
    choice = models.IntegerField()

    class Meta:
        db_table = "choice_check"

class Emotion(models.Model):
    id = models.AutoField(primary_key=True)
    face = models.FloatField()
    voice = models.FloatField()
    brain = models.FloatField()
    user = models.CharField(max_length=200)
    createAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "emotion"

class AuthSms(models.Model):
    auth_phone = models.CharField(max_length=11, primary_key=True)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'auth_sms'


class AuthEmail(models.Model):
    auth_email = models.CharField(max_length=200, primary_key=True)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'auth_email'


class Auth_Category(models.Model):
    auth_name = models.CharField(max_length=200)
    auth_explain = models.CharField(max_length=400, null=True)
    auth_path = models.CharField(max_length=400, null=True)
    auth_yn = models.BooleanField()

    class Meta:
        db_table = 'auth_category'




# class User(models.Model):
#     user_seq = models.BigIntegerField(primary_key=True)
#     user_email = models.CharField(max_length=45)
#     user_pw = models.CharField(max_length=45)  # 유저 비밀번호
#     user_nm = models.CharField(max_length=45)  # 유저 이름
#     user_phone = models.CharField(max_length=45)
#     user_createAt = models.DateTimeField(auto_now=True)  # 저장된 레코드 수정 시 수정 시각
#
#     def __str__(self):
#         return "%s %s %s %s %s" % (self.user_nm, self.user_pw, self.user_email, self.user_phone, self.user_createAt)
#
#
# class Security(models.Model):
#     security_seq = models.BigIntegerField(primary_key=True)
#     security_nm = models.CharField(max_length=45)  # 보안 종류 이름
#
#     def __str__(self):
#         return "%s" % self.security_nm
#
#
# class User_Security(models.Model):
#     user_security_seq = models.BigIntegerField(primary_key=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)  # User 인스턴스
#     security = models.ForeignKey(Security, on_delete=models.CASCADE)  # Security 인스턴스
#     security_yn = models.CharField(max_length=45)  # User별 보안 설정 여부
#
#     def __str__(self):
#         return "%s %s" % (self.security, self.security_yn)

# class Auth(TimeStampedModel):
#     phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
#     auth_number = models.IntegerField(verbose_name='인증 번호')
#
#     class Meta:
#         db_table = 'auth'
#
#         def save(self, *args, **kwargs):
#             self.auth_number = randint(1000, 1000)
#             super().save(*args, **kwargs)
#             self.send_sms()
#
#         def send_sms(self):
#             url = 'https://api-sens.ncloud.com/v1/sms/services/{serviceId}/messages/'
#
#             data = {
#                 "type": "SMS",
#                 "from": "01012345678",
#                 "to": [self.phone_number],
#                 "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number)
#             }
#             headers = {
#                           "Content-Type": "application/json",
#                           # "x-ncp-auth-key": {Sub Account Access Key},
#                           # "x-ncp-service-secret": {SMS Service Secret},
#             }
#             requests.post(url, json=data, headers=headers)

