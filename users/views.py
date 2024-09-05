from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from main.models import UserProfile
from .forms import CoverUpdateForm, ProfilePicUpdateForm
from django.http import HttpResponse
from django.utils.crypto import get_random_string
import os


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


@login_required
def updateCover_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        print('Form submission detected')
        form = CoverUpdateForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            print('Form is valid')
            cover = request.FILES.get('user_cover')
            
            if cover:
                # Debugging file properties
                print(f"File name: {cover.name}")
                print(f"File content_type: {cover.content_type}")
                print(f"File size: {cover.size}")

                # Generate a unique filename and save
                random_str = get_random_string(8) 
                file_name, file_extension = os.path.splitext(cover.name)
                print(f"File extension: {file_extension}")

                # In case no extension is detected
                if not file_extension:
                    print("No valid file extension detected")
                    # Handle the error (return form invalid)
                    form.add_error('user_cover', 'File does not have a valid extension.')
                    return render(request, 'users/profile.html', {'form': form})
                
                new_filename = f"cover_{random_str}{file_extension}"
                user_profile.user_cover.name = f'{new_filename}'
                user_profile.save()

            return redirect('profile', user_id=user.id)
           
        else:
            print('Form is invalid') 
            print(form.errors)
            return redirect('profile', user_id=user.id)

    return redirect('profile', user_id=user.id)


@login_required
def updateProfileImage_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        print('Form submission detected')
        form = ProfilePicUpdateForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            print('Form is valid')
            u_image = request.FILES.get('user_image')
            
            if u_image:
                # Debugging file properties
                print(f"File name: {u_image.name}")
                print(f"File content_type: {u_image.content_type}")
                print(f"File size: {u_image.size}")

                # Generate a unique filename and save
                random_str = get_random_string(8) 
                file_name, file_extension = os.path.splitext(u_image.name)
                print(f"File extension: {file_extension}")

                # In case no extension is detected
                if not file_extension:
                    print("No valid file extension detected")
                    # Handle the error (return form invalid)
                    form.add_error('user_image', 'File does not have a valid extension.')
                    return render(request, 'users/profile.html', {'form': form})
                
                new_filename = f"profile_{random_str}{file_extension}"
                user_profile.user_image.name = f'{new_filename}'
                user_profile.save()

            return redirect('profile', user_id=user.id)
           
        else:
            print('Form is invalid') 
            print(form.errors)
            return redirect('profile', user_id=user.id)

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



