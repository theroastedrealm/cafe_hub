from django.db import models

class ProductService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.BinaryField(editable=True)
    video = models.BinaryField(null=True, blank=True, editable=True)
    link = models.URLField()

    def __str__(self):
        return self.name