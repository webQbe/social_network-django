from django import forms
from main.models import UserProfile
from .models import Post, Comment
from django.contrib.auth.models import User


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
    
class ProfilePicUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_image'] # Add profile image to the form

    def clean_profilePic(self):
        u_image = self.cleaned_data.get('user_image', False)
        if not u_image:
            raise forms.ValidationError("Please upload a valid profile image.")
        if u_image and not u_image.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Only .png, .jpg, and .jpeg formats are allowed.")
        return u_image
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_content', 'upload_image', ] 

    def clean_postImage(self):
        p_image = self.cleaned_data.get('upload_image', False)
        if not p_image:
            raise forms.ValidationError("Please upload a valid post image.")
        if p_image and not p_image.name.endswith(('.png', '.jpg', '.jpeg')):
            raise forms.ValidationError("Only .png, .jpg, and .jpeg formats are allowed.")
        return p_image
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_birthday', 'describe_user', 'relationship', 'user_country', 'user_gender', 'recovery_answer']
        widgets = {
            'user_birthday':forms.DateInput(attrs={'type':'date'}),
        }

    
class ForgotPasswordForm(forms.Form):    
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = [ 'email', 'recovery_answer',]


class ChangePasswordForm(forms.Form):    
    password = forms.CharField(required=True, label='New Password')
    password2 = forms.CharField(required=True, label='Confirm Password')

    class Meta:
        model = User
        fields = [ 'password']
