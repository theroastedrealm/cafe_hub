from django.db import models
from django.contrib.auth.models import AbstractUser , Group
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=10,blank=True, null=True)  
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser): 
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        
    ]

    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')    
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
   

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'uber-user'
            self.is_staff = True
        elif self.role in ['admin', 'uber-user']:
            self.is_staff = True
        else:
            self.is_staff = False
        super(CustomUser, self).save(*args, **kwargs)


class FavoriteCafes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

