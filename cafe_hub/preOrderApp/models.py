from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

from main.models import Branch

class Category(models.Model):
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, related_name='categories', on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, related_name='items', on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.name

class Order(models.Model):
    order_status = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('finished', 'Finished'),
    ]
    order_number = models.CharField(max_length=100)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)
    status = models.CharField(max_length=10, choices=order_status, default='pending')
    branch = models.ForeignKey(Branch, related_name='orders', on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"