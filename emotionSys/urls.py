from django.urls import path
from . import views
from .views import AuthSmsView, v2_phoneCheck

urlpatterns = [
    # path('main', views.main, name='main'),
    # path('main2', views.main2, name='main2'), # 예시 나중에 삭제
    # path('emotion', views.emotion, name='emotion'),
    # path('face2', views.emotion_face, name='emotion_face'),
    # path('emotion/result', views.emotion_result, name='emotion_result'),
    # path('signIn', views.signIn, name='signIn'),
    # path('signOut', views.signOut, name='signOut'),
    # path('phone', views.phone, name='phone'),
    # # path('singUp/', views.singUp, name='singUp'),
    # path('dashBoard', views.dashBoard, name='dashBoard'),
    # path('re_auth', views.re_auth, name='re_auth'),
    # path('userlog', views.user_log, name='user_log'),
    # path('emailsign', views.email_sign),
    # path('users/check', views.activate),
    # path('authSms', AuthSmsView.as_view()),
    # path('authSms/check', views.check_sms),check_sms


    path('v2/main', views.v2_main, name='v2_main'),
    path('v2/signIn', views.v2_signIn, name='v2_signIn'),
    path('v2/userLog', views.v2_userlog, name='v2_userlog'),
    path('v2/userManager', views.v2_userManager, name='v2_userManager'),
    path('v2/faceLog', views.v2_facelog, name='v2_facelog'),
    path('v2/voiceLog', views.v2_voicelog, name='v2_voicelog'),
    path('v2/emotionLog', views.v2_emotionlog, name='v2_emotionlog'),
    path('v2/failLog', views.v2_faillog, name='v2_faillog'),
    path('v2/signOut', views.v2_signOut, name='v2_signOut'),
    path('v2/signUp', views.v2_signUp, name='v2_signUp'),
    path('v2/fail', views.v2_fail, name='v2_fail'),
    path('v2/emailCheck', views.v2_emailCheck, name='v2_emailCheck'),
    path('v2/phoneCheck', v2_phoneCheck.as_view(), name='v2_phoneCheck'),
    # path('v2/locateCheck', views.v2_locateCheck, name='v2_locateCheck'),
    # path('v2/emotionCheck', views.v2_emotionCheck, name='v2_emotionCheck'),
    # admin 기능 관리자 페이지 --> 추후 사용자, 관리자로 분리
    path('v2/dashBoard', views.v2_dashBoard, name='v2_dashBoard'),
    # admin 기능 보안 기능 선택 (ajax로 구현)
    # path('v2/checkChoice', views.v2_checkChoice, name='v2_checkChoice'),
]