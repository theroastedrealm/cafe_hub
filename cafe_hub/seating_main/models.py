from django.db import models
from django.conf import settings
from django.db import models
from django.conf import settings
from main.models import Branch


# Create your models here.
class Seat(models.Model):
    name = models.CharField(max_length=15)
    available = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
