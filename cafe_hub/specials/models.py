from django.db import models

from main.models import Branch

# Create your models here.
class Special(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)