from django.contrib import admin
from django.urls import path, include

from seating_main import views as v
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    
    path('', v.homepage, name="seating_homepage"),
    path('update_seat_availability/<int:seat_id>', v.update_seat_availability, name="update_seat_availability"),
    
    
    
    path('staff/', v.staffpage, name="staffpage"),
    path('staff_update_seat_availability/<int:seat_id>', v.staff_update_seat_availability, name="staff_update_seat_availability"),
    path('staff_add_seat/', v.staff_add_seat, name="staff_add_seat"),
    path('staff_delete_seat/<int:seat_id>', v.staff_delete_seat, name="staff_delete_seat"),
]
