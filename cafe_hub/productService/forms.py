from django import forms
from .models import ProductService

class ProductServiceForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    video = forms.FileField(required=False)

    class Meta:
        model = ProductService
        fields = ['name', 'description', 'link']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get('image'):
            instance.image = self.cleaned_data['image'].read()
        if self.cleaned_data.get('video'):
            instance.video = self.cleaned_data['video'].read()
        if commit:
            instance.save()
        return instance