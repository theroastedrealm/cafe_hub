from django.contrib import admin
from django.urls import path
from .views import Index, Dashboard, AddItem, EditItem, DeleteItem

urlpatterns = [
    # path('', Index.as_view(), name='index'),
    path('', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
]
