 #main/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from main.models import CustomUser
from .models import Branch

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    #branch = forms.ModelChoiceField(queryset=Branch.objects.all(), label="Select Branch")

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'role']


class CombinedForm(forms.Form):
    def __init__(self):
        self.signup_form = SignUpForm()
        self.login_form = AuthenticationForm()

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'address', 'city', 'zip_code']


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)