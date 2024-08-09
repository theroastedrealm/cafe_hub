from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from main.models import Branch

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
    order_date = models.DateField(null=True, blank=True)  
    next_order = models.IntegerField(null=True, blank=True)  

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.name
    