from django.urls import path
from . import views

urlpatterns = [
    path('v2/demo_login', views.v2_demo_login, name='v2_demo'),
    path('v2/demo_logOut', views.v2_demo_logOut, name='v2_demo'),
    path('v2/demo', views.v2_demo, name='v2_demo'),
    path('v2/demo_info', views.v2_demo_info, name='v2_demo_info'),
    path('v2/demo_certification', views.v2_demo_certification, name='v2_demo_certification'),
    path('v2/demo_encryption', views.v2_demo_encryption, name='v2_demo_encryption'),
    path('v2/emailCheck', views.v2_emailCheck, name='v2_emailCheck'),
    path('v2/phoneCheck', views.v2_phoneCheck.as_view(), name='v2_phoneCheck'),
    path('v2/patternCheck', views.v2_patternCheck, name='v2_patternCheck'),
    path('v2/questionCheck', views.v2_questionCheck, name='v2_questionCheck'),
]