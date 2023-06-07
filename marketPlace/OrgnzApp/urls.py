from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'OrgnzApp'



urlpatterns = [


        path('Organizerlogin/', views.login1, name='login1'),

        path('Organizerlogout/', views.logout, name='logout'),
        path('orgSuccessful/', views.orgSuccessful, name='orgSuccessful'),

        path('orgRegister/', views.orgRegister, name='orgRegister'),

        path('Orgprofile/', views.profile, name='profile'),
        path('OrgchangeProfile/', views.changeProfile, name='changeProfile'),
        path('OrgchangePass/', views.changePass, name='changePass'),

        path('burn/', views.burn, name='burn'),
        path('burnSuccessful/', views.burnSuccessful, name='burnSuccessful'),
        path('burnfaild/', views.burnfaild, name='burnfaild'),
        path('burnList/', views.burnList, name='burnList'),
        path('showticket/', views.showticket, name='showticket'),
        path('createNFT/', views.createNFT, name='createNFT'),
        path('sold/', views.sold, name='sold'),
        path('notSold/', views.notSold, name='notSold'),






        ]
