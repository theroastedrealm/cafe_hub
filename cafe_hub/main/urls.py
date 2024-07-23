# main/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import branch_detail, create_branch



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('branches/new/', views.create_branch, name='create_branch'),
     path('search/', views.search, name='search'),
      path('branch/<int:branch_id>/', branch_detail, name='branch_detail'),
]
