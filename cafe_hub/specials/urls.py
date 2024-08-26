from django.contrib import admin
from django.urls import path, include

from specials import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    
    path('', views.homepage, name="specials_homepage"),
    path('create/', views.create_special, name="create_special"),
    path('delete/<int:special_id>/', views.delete_special, name="delete_special"),

]