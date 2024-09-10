from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from main.models import UserProfile
from .models import Post, Comment
from .forms import CoverUpdateForm, ProfilePicUpdateForm, PostForm, CommentForm
from django.http import HttpResponse
from django.utils.crypto import get_random_string
import os
from django.middleware.csrf import CsrfViewMiddleware
from django.core.files.storage import default_storage
from django.core.paginator import Paginator


# Create your views here.

@login_required(login_url='/')
def home_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # fetch all posts
    posts = Post.objects.all().order_by('-post_date')

    # pagination
    per_page = 4 # Posts per page

    # Pagination logic
    all_pages = Paginator(posts, per_page) 
    page_number = request.GET.get('page', 1)
    page = all_pages.get_page(page_number)

    context = {
        'posts':page,
        'user_profile':user_profile,
        'logged_in_user': request.user, 
    }
    return render(request, 'users/home.html', context)


@login_required(login_url='/')
def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    # latest 5 posts
    posts = Post.objects.filter(user=user).order_by('-post_date')[:5]

    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'logged_in_user': request.user, 
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


@login_required
def create_post_view(request):
    if request.method == 'POST':
       content = request.POST.get('post_content', '').strip()
       upload_image = request.FILES.get('upload_image')

       # Generate a random number for the image name
       random_number = get_random_string(8)
       
       # Image handling
       if upload_image:
           # Construct a new filename
           _, extension = os.path.splitext(upload_image.name)
           new_filename = f"{upload_image.name.split('.')[0]}_{random_number}{extension}"
           
           # Save the uploaded image
           image_path = f"imagepost/{new_filename}"
           default_storage.save(image_path, upload_image)

       # Validate content length
       if len(content) > 250:
           return render(request, 'users/home.html', {
               'form':PostForm(),
                'error':"Please use 250 or fewer characters!"})

        # Check conditions for post submission
       if upload_image and content:
           # Save both content and image
           post = Post(user=request.user, post_content=content, upload_image=image_path)
           post.save()
           # update the user's post status
           request.user.userprofile.posts = "Yes"
           request.user.userprofile.save()
         

       elif content == '' and upload_image:
           # Only image is provided, save the image
           post = Post(user=request.user, upload_image=image_path)
           post.save()
           # update the user's post status
           request.user.userprofile.posts = "Yes"
           request.user.userprofile.save()


       elif content:
           # Only content is provided, no image
           post = Post(user=request.user, post_content=content)
           post.save()
           # update the user's post status
           request.user.userprofile.posts = "Yes"
           request.user.userprofile.save()

       else:
           return redirect('home')
       
       # Redirect after saving the post
       return redirect('home')
    
    # If it's not a POST request, render the form
    return render(request, 'users/home.html', {'form':PostForm()})
              

@login_required
def post_delete_home(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, user=request.user)
    post.delete()
    return redirect('home')

@login_required
def post_delete_profile(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, user=request.user)
    post.delete()
    return redirect('profile', user_id=request.user.id)

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, post_id=post_id, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('post_content')
        post.post_content = content
        post.save()

        messages.success(request, 'Post has been updated successfully!')
        return redirect('profile', user_id=request.user.id)
    
    context = {
        'post':post,
    }
    return render(request, 'users/edit_post.html', context)

@login_required
def single_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    context = {
        'post':post,
        'form':CommentForm(),
        'comments': Comment.objects.filter(post=post).order_by('-date'),
        'user_profile':user_profile,
    }

    return render(request, 'users/single_post.html', context)


@login_required
def comment_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
       comment_text = request.POST.get('comment', '').strip()

       # Validate content length
       if len(comment_text) > 250:
           return render(request, 'users/single_post.html', {
               'form': CommentForm(),
                'error': "Please use 250 or fewer characters!",
                'post': post,
                'comments': Comment.objects.filter(post=post).order_by('-date')
                })
       
       # Save the comment
       comment = Comment.objects.create(
            post=post,
            user=request.user,
            comment=comment_text,
            comment_author=request.user.username
        )
       
       # Redirect after saving the post
       return redirect('single_post', post_id=post_id)
    
    context = {
            'post' : post,
            'form' : CommentForm,
            'comment':Comment.objects.filter(post=post).order_by('-date'),
        }
    
    return render(request, 'users/single_post.html', context)
    
  

@login_required
def logout_view(request):
    logout(request)
    return redirect('main_page')

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

def csrf_failure(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})



