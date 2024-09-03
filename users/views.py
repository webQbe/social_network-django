from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View

# Create your views here.

@login_required
def home_view(request):
    return render(request, 'users/home.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')