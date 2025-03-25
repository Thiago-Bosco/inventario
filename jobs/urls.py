from django.urls import path
from . import views
from django.urls import path
from django.shortcuts import render
from .views import dashboard , hardware


urlpatterns = [
    path('', views.index, name='index'),
    path('all_servers/', views.show_all_servers, name='all_servers'),
    path('all_FastShop/', views.show_all_fastshop, name='all_FastShop'),
    path('ajuda/', views.ajuda, name='ajuda'),
    path('all_jobs/', views.show_all_jobs, name='all_jobs'),
    path('dashboard/', dashboard, name='dashboard'),
    path('hard/', hardware, name='hard'),


]