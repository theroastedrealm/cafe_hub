# main/urls.py
from django.urls import path

from inventory.views import Dashboard
from . import views
from django.contrib.auth import views as auth_views
from .views import branch_detail, create_branch



urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.branchesView, name='index'),
    path('homepage/', views.index,name='housingpage'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('branches/new/', views.create_branch, name='create_branch'),
    path('search/', views.search, name='search'),
    path('branch/<int:branch_id>/', branch_detail, name='branch_detail'),
    path('redirect-to-admin/', views.redirect_to_admin, name='redirect_to_admin'),
    path('redirect-admin/<str:branch_name>/', views.redirect_to_branch_admin, name='redirect_admin'),
    path('branches/', views.branchesView, name='branches'),
    path('set_current_branch/<int:branch_id>/', views.set_current_branch, name='set_current_branch'),
    path('add-to-favorites/<int:branch_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:branch_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]




