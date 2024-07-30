"""
URL configuration for cafe_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from preOrderApp.views import Menu
from inventory.views import Dashboard
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('main.urls')), 
    path('', views.index, name='index'),
    path('menu/',include('preOrderApp.urls')),
    path('seating/',include('seating_main.urls')),
    path('inventory/', include('inventory.urls')),
    #path('branch/<int:pk>/', views.branch_detail, name='branch_detail'),
    #path('branch/<int:pk>/menu/', Menu.as_view(), name='menu'),
    #path('branch/<int:pk>/inventory/',Dashboard.as_view() , name='inventory'),
]


