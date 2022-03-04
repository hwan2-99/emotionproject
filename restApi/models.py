# from django.db import models
#
#
# # Create your models here.
#
# class User(models.Model):
#     user_seq = models.BigIntegerField(primary_key=True)
#     user_pw = models.CharField(max_length=45)  # 유저 비밀번호
#     user_email = models.CharField(max_length=45)
#     user_nm = models.CharField(max_length=45)  # 유저 이름
#
#     user_createAt = models.DateTimeField(auto_now=True)  # 저장된 레코드 수정 시 수정 시각
#
#     def __str__(self):
#         return "%s %s %s" % (self.user_pw, self.user_nm, self.user_createAt)
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
#     user = models.ForeignKey(User, on_delete=models.CASCADE)    # User 인스턴스
#     security = models.ForeignKey(Security, on_delete=models.CASCADE)  # Security 인스턴스
#     security_yn = models.CharField(max_length=45)   # User별 보안 설정 여부
#
#     def __str__(self):
#         return "%s %s" % (self.security, self.security_yn)
