from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('voice', views.voice, name='voice'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('v2/voice', views.voice, name='voice'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('face', views.face, name='face'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('v2/face', views.face, name='face'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('gps', views.gps, name='gps'),  # GPS를 3개까지 저장하고, GPS가 유효한지 판단하는 view로 Request를 넘김
    path('v2/gps', views.gps, name='gps'),  # GPS를 3개까지 저장하고, GPS가 유효한지 판단하는 view로 Request를 넘김
    path('ip', views.ip, name='ip'), # IP를 3개까지 저장하고, IP가 유효한지 판단하는 view로 Request를 넘김
    path('v2/ip', views.ip, name='ip'), # IP를 3개까지 저장하고, IP가 유효한지 판단하는 view로 Request를 넘김
    path('mypage/emotion', views.mypage_emotion, name="mypage_emotion"),
    path('choice-check', views.choice_check, name="choice_check"),
    path('encryption-algorithm', views.encryption_algorithm, name="encryption_algorithm"),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]