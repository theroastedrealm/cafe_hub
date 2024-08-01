from django.contrib import admin

from main.models import Branch
from .models import InventoryItem, Category

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'category','branch']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(branch=request.user.branch)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['branch'].queryset = Branch.objects.filter(id=request.user.branch.id)
        return form
    
admin.site.register(InventoryItem, InventoryItemAdmin)


class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','branch']
   
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(branch=request.user.branch)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['branch'].queryset = Branch.objects.filter(id=request.user.branch.id)
        return form
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.branch = request.user.branch
        super().save_model(request, obj, form, change)
    
admin.site.register(Category, InventoryCategoryAdmin)