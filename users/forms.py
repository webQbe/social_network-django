from django import forms
from main.models import UserProfile

class CoverUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_cover']