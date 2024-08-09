# admin.py
from django import forms
from django.contrib import admin
from .models import Branch, CustomUser
from django.contrib.auth.models import Group
from django.contrib.admin import AdminSite


class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'address','city', 'zip_code']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        if request.user.branch:
            return qs.filter(id=request.user.branch.id)
        else:
            return qs.none()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if request.user.branch:
                form.base_fields['branch'].queryset = Branch.objects.filter(id=request.user.branch.id)
            else:
                form.base_fields['branch'].queryset = Branch.objects.none()
        return form

admin.site.register(Branch, BranchAdmin)

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

group, created = Group.objects.get_or_create(name='admin')
group, created = Group.objects.get_or_create(name='uber-user')
group, created = Group.objects.get_or_create(name='customer')

group.save()

class BranchAdminSite(AdminSite):
    site_header = "Coffee Shop Admin"
    site_title = "Manager Portal"
    index_title = "Welcome to the Admin Portal"
    
branch_admin_site = BranchAdminSite(name='branch_admin')
branch_admin_site.register(Branch, BranchAdmin)





