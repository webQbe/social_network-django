from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):    
    u_pass = forms.CharField(widget=forms.PasswordInput, label='Password')
    u_email = forms.EmailField(required=True, label='Email')
    u_country = forms.ChoiceField(choices=[('Sri Lanka', 'Sri Lanka'), ('Pakistan', 'Pakistan'), ('USA', 'USA'), ('India', 'India'), ('Japan', 'Japan'), ('UK', 'UK'), ('Russia', 'Russia')], label='Country')
    u_gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], label='Gender')
    u_birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Birthday')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'u_pass',  'u_email', 'u_country', 'u_gender', 'u_birthday', ]

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['u_pass'])
        user.email = self.cleaned_data['u_email']
        if commit:
            user.save()
        return user