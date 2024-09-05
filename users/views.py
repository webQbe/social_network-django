from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from main.models import UserProfile
from .forms import CoverUpdateForm


# Create your views here.

@login_required(login_url='/')
def home_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    context = {
        'user_profile':user_profile,
    }
    return render(request, 'users/home.html', context)


@login_required(login_url='/')
def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    return render(request, 'users/profile.html', context)


@login_required(login_url='/')
def updateCover_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = CoverUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
        else:
            return render(request, 'users/profile.html', {'form':form, 'user_profile':user_profile})

    return redirect('profile', user_id=user.id)

@login_required(login_url='/')
def find_view(request):
    return render(request, 'users/find_people.html')

@login_required(login_url='/')
def message_view(request):
    return render(request, 'users/message.html')

@login_required(login_url='/')
def myPosts_view(request, user_id):
    user_posts = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'users/myposts.html', {'user_posts':user_posts})

@login_required(login_url='/')
def editProfile_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'users/edit_profile.html', {'user_profile':user_profile})

@login_required(login_url='/')
def search_view(request):
    return render(request, 'users/search.html')



