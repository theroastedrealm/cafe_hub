from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_service_list, name='product_service_list'),
    path('add/', views.product_service_add, name='product_service_add'),
    path('edit/<int:pk>/', views.product_service_edit, name='product_service_edit'),
    path('delete/<int:pk>/', views.product_service_delete, name='product_service_delete'),
    path('confirm_delete/<int:pk>/', views.product_service_confirm_delete, name='product_service_confirm_delete'), 
]