from django.db import models
from django.core.management.base import BaseCommand
from django.contrib.auth.models import AbstractUser , Group, Permission
from django.contrib.contenttypes.models import ContentType





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
        ('uber-user', 'Uber-User')
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


