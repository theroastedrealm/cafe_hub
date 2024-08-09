from django.urls import path

from django.contrib import admin
from . import views


urlpatterns = [
    path('admin_page/', views.admin_page, name='admin_page'),
    path('menu_page/', views.menu_page, name='menu_page'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]