from django.urls import path
from .views import add_product, product_list, productHomepage
from choiceProducts import views

urlpatterns = [
    path('',views.productHomepage,name='product_homepage'),
    path('create/',views.add_product,name='add_product'),
    path('delete/<int:product_id>/', views.delete_product, name="delete_product"),
    path('choiceproductslist/',product_list,name ='product_list'),

]