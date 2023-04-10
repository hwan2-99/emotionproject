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
    path('v2/demo_analyze', views.v2_demo_analyze, name='v2_demo_analyze'),
    path('v2/demo_analyze_face', views.v2_demo_analyze_face, name='v2_demo_analyze_face'),
    path('v2/demo_analyze_voice', views.v2_demo_analyze_voice, name='v2_demo_analyze_voice'),
    path('v2/demo_analyze_brain', views.v2_demo_analyze_brain, name='v2_demo_analyze_brain'),
    path('v2/demo_analyze_graph', views.v2_demo_analyze_graph, name='v2_demo_analyze_graph'),
    path('demo_voice', views.demo_voice, name='demo_voice'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('v2/demo_voice', views.demo_voice, name='demo_voice'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('demo_face', views.demo_face, name='demo_face'),  # User에 관한 API를 처리하는 view로 Request를 넘김
    path('v2/demo_face', views.demo_face, name='demo_face'),  # User에 관한 API를 처리하는 view로 Request를 넘김
]
