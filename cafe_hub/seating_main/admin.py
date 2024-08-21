from django.contrib import admin
from .models import Seat
from main.models import Branch

# Register your models here.
class SeatAdmin(admin.ModelAdmin):
    list_display=['name','available','branch']
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
admin.site.register(Seat, SeatAdmin)