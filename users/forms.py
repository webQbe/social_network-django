from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['f_name', 'l_name', 'user_name', 'user_email', 'password', 'user_country', 'user_gender', 'user_birthday']