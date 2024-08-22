from django.conf import settings
from django.db import models

from main.models import Branch

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username