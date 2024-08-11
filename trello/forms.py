from django.forms import ModelForm
from .models import Company
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
