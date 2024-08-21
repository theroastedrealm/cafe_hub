from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('create/', views.create_post, name='create_post'),
    path('profile/', views.profile_page, name='profile_page'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/add/', views.add_comment, name='add_comment'),
    path('user/<int:user_id>/', views.user_posts, name='user_posts'),
]
