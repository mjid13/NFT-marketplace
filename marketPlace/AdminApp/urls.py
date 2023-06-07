from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'AdminApp'


urlpatterns = [


        path('index/', views.index, name='index'),




        path('registerType/', views.registerType, name='registerType'),

        path('about/', views.about, name='about'),
        path('activity/', views.activity, name='activity'),
        path('help/', views.help, name='help'),
        path('contatct/', views.contatct, name='contatct'),


        path('adminlogin/', views.adminLogin, name='adminlogin'),
        path('adminlogout/', views.logout, name='adminlogout'),

        path('adminpage/', views.adminPage, name='adminpage'),
        path('adminpageOrg/', views.adminPageOrg, name='adminpageOrg'),
        path('adminpageUser/', views.adminPageUser, name='adminpageUser'),

        path('mart/', views.mart, name='mart'),
        path('search/', views.search, name='search'),
        path('doneBuy/', views.doneBuy, name='doneBuy'),
        path('collectionTicket/', views.collectionTicket, name='collectionTicket'),
        path('SingleTicket/', views.singleTicket, name='singleTicket'),



        ]

