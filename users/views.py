from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from main.models import UserProfile
#from .models import UserPosts

# Create your views here.

@login_required
def home_view(request):
    return render(request, 'users/home.html')

@login_required
def profile_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    return render(request, 'users/profile.html', {'user': user, 'user_profile': user_profile})

@login_required
def find_view(request):
    return render(request, 'users/find_people.html')

@login_required
def message_view(request):
    return render(request, 'users/message.html')

@login_required
def myPosts_view(request, user_id):
    user_posts = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'users/myposts.html', {'user_posts':user_posts})

@login_required
def editProfile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'users/edit_profile.html', {'user_profile':user_profile})

@login_required
def search_view(request):
    return render(request, 'users/search.html')



