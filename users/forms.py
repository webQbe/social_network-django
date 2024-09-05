from django import forms
from main.models import UserProfile

class CoverUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_cover'] # Add user_cover to the form

    def clean_user_cover(self):
        cover = self.cleaned_data.get('user_cover', False)
        if not cover:
            raise forms.ValidationError("Please upload a valid cover image.")
        if cover and not cover.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Only .png, .jpg, and .jpeg formats are allowed.")
        return cover