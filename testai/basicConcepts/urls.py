from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Welcome, name='Welcome'),
    path('user', views.User, name='User'),
    path('IrisApp/', include('IrisApp.urls'))
]   