from django.contrib import admin
from django.contrib.admin import AdminSite
from main.models import Branch, CustomUser
from .models import InventoryItem, Category

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category','branch']
    
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
            form.base_fields['branch'].queryset = Branch.objects.filter(id=request.user.branch.id)
            form.base_fields['user'].queryset = CustomUser.objects.filter(id=request.user.id)
        return form
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user 
            obj.branch = request.user.branch
        super().save_model(request, obj, form, change)

admin.site.register(InventoryItem, InventoryItemAdmin)


class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch']
    fields = ['name', 'branch']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(branch=request.user.branch)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if request.user.branch:
                form.base_fields['branch'].queryset = Branch.objects.filter(id=request.user.branch.id)
            else:
                form.base_fields['branch'].queryset = Branch.objects.none()
        return form

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.branch = request.user.branch
        super().save_model(request, obj, form, change)

admin.site.register(Category, InventoryCategoryAdmin)