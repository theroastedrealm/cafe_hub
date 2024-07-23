from django.db import models
from django.conf import settings

# Create your models here.
class Seat(models.Model):
    name = models.CharField(max_length=15)
    available = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
