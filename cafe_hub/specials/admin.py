from django.contrib import admin

from main.models import Branch
from .models import Special
# Register your models here.
class SpecialsAdmin(admin.ModelAdmin):
    list_display=['name','description','image','branch']
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
admin.site.register(Special, SpecialsAdmin)