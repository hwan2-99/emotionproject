from django.urls import path
from . import views

urlpatterns = [
    path('v2/demo', views.v2_demo, name='v2_demo'),
]