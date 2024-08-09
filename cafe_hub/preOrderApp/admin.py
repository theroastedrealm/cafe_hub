from django.contrib import admin


from main.models import Branch
from preOrderApp.models import Item,Category,Order

# Register your models here.


class preOrderItemAdmin(admin.ModelAdmin):
    list_display=['name','category','branch']
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
admin.site.register(Item, preOrderItemAdmin)


class preOrderCategoryAdmin(admin.ModelAdmin):
    list_display=['name','branch']
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
admin.site.register(Category, preOrderCategoryAdmin)


class orderAdmin(admin.ModelAdmin):
    list_display=['order_number','customer','status','branch']
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
admin.site.register(Order, orderAdmin)