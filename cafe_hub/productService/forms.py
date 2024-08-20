from django import forms
from .models import ProductService

class ProductServiceForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = ProductService
        fields = ['name', 'description', 'link', 'image', 'video']

    