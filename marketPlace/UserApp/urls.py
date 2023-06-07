from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'UserApp'


urlpatterns = [
        path('Uesrlogin/', views.login1, name='login'),

        path('logout1/', views.logout, name='logout'),


        path('userRegister/', views.userRegister, name='userRegister'),

        path('profile/', views.profile, name='profile'),
        path('changeProfile/', views.changeProfile, name='changeProfile'),
        path('changePass/', views.changePass, name='changePass'),

        path('MyTicket/', views.myTicket, name='myTicket'),



        ]

