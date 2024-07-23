# admin.py
from django import forms
from django.contrib import admin
from .models import Branch, CustomUser
from django.contrib.auth.models import Group

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'address','city', 'zip_code']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role','branch']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #Allow superusers to see all branches
        if request.user.is_superuser:
            return qs
        # Restrict other users to only see their own branch
        return qs.filter(branch=request.user.branch)







