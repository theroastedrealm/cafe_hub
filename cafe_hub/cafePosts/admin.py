from django.contrib import admin

from main.models import Branch
from .models import Post, Comment, UserProfile


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'content', 'created_at', 'updated_at','branch']
    
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
        return form
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','author', 'content', 'created_at', 'updated_at','branch']
    
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
        return form
    
admin.site.register(Comment, CommentAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'birth_date', 'profile_pic', 'created_at']
    
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
        return form
    
admin.site.register(UserProfile, UserProfileAdmin)