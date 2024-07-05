from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index),
    path('result', views.formInfo, name = 'result'),
    path('save_photo/', views.save_photo, name='save_photo')
]