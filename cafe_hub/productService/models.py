from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os

from main.models import Branch

class ProductService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='productService/images/', editable=True) 
    video = models.FileField(upload_to='productService/videos/', null=True, blank=True, editable=True)
    link = models.URLField()
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=False, blank=False, default=1)
    def __str__(self):
        return self.name

@receiver(post_delete, sender=ProductService)
def delete_product_service_image(sender, instance, **kwargs):
    if instance.image and hasattr(instance.image, 'path'):
        image_path = os.path.join(settings.MEDIA_ROOT, instance.image.path)
        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Deleted image at {image_path}")
            except Exception as e:
                print(f"Error deleting image at {image_path}: {e}")