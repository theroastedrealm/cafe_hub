from django.db import models

from main.models import Branch

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    amazon_link = models.URLField(max_length=500)
    added_at = models.DateTimeField(auto_now_add=True)
    branch = models.ForeignKey(Branch, related_name='product', on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.name