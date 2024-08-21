from django import forms
from .models import InventoryItem, Category, Branch

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category', 'branch']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(InventoryItemForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
             self.fields['branch'].queryset = Branch.objects.filter(id=user.branch.id)