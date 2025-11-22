from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from main.models import UserProfile
from .models import Post, Comment, Message
from .forms import CoverUpdateForm, ProfilePicUpdateForm, PostForm, CommentForm, EditUserForm, EditUserProfileForm, ForgotPasswordForm, ChangePasswordForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils.crypto import get_random_string
import os
from django.middleware.csrf import CsrfViewMiddleware
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db import models
from django.contrib.auth.hashers import make_password



# Create your views here.

@login_required(login_url='/')
def home_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    # fetch all posts
    posts = Post.objects.all().order_by('-post_date')

    post_count = Post.objects.filter(user=user_profile.user).count()

    # pagination
    per_page = 4 # Posts per page

    # Pagination logic
    paginator = Paginator(posts, per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts':page_obj,  # Contains the paginated posts
        'user_profile':user_profile,
        'logged_in_user': request.user,
        'post_count' : post_count,
    }
    return render(request, 'users/home.html', context)


@login_required(login_url='/')
def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    # latest 5 posts
    posts = Post.objects.filter(user=user).order_by('-post_date')[:5]

    post_count = Post.objects.filter(user=user_profile.user).count()

    is_own_profile = (request.user == user)
    is_following = user_profile.following.filter(pk=request.user.pk).exists()
    follower_count = user_profile.following.count()

    context = {
        'user': user,
        'user_profile': user_profile,
        'posts': posts,
        'logged_in_user': request.user, 
        'post_count' : post_count,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'follower_count': follower_count,
    }

    return render(request, 'users/profile.html', context)

@login_required
def toggle_follow_view(request, user_id):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")
    
    target_user = get_object_or_404(User, pk=user_id)
    # prevent following user's own profile
    if request.user == target_user:
        messages.error(request, "You cannot follow yourself.")
        return redirect(request.POST.get('next') or request.META.get('HTTP_REFERER') or '/')

    target_profile = get_object_or_404(UserProfile, user=target_user)

    # Efficient existence check
    if target_profile.following.filter(pk=request.user.pk).exists():
        target_profile.following.remove(request.user)
    else:
        target_profile.following.add(request.user)

    # redirect back to profile page (or use 'next' POST param)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)

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
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        content = request.POST.get('post_content')
        post.post_content = content
        post.save()

        messages.success(request, 'Post has been updated successfully!')
        return redirect('profile', user_id=request.user.id)
    
    post_count = Post.objects.filter(user=user_profile.user).count()
    
    context = {
        'post':post,
        'post_count': post_count,
    }
    return render(request, 'users/edit_post.html', context)

@login_required
def single_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    post_count = Post.objects.filter(user=user_profile.user).count()

    context = {
        'post':post,
        'form':CommentForm(),
        'comments': Comment.objects.filter(post=post).order_by('-date'),
        'user_profile':user_profile,
        'post_count' : post_count,
        
    }

    return render(request, 'users/single_post.html', context)

@login_required
def comment_post_view(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
       comment_text = request.POST.get('comment', '').strip()

       if not comment_text:
           messages.error(request, "Please write something!")
           return redirect('single_post', post_id=post_id)
       
       # Validate content length
       if len(comment_text) > 250:
           messages.error(request, "Please use 250 or fewer characters!")
           return redirect('single_post', post_id=post_id)
       
       # Save the comment
       Comment.objects.create(
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
            'user_profile': user_profile,
        }
    
    return render(request, 'users/single_post.html', context)

@login_required
def like_post_view(request, post_id):
    """  Toggle like/unlike for the logged in user on given post.
         Accepts POST requests only. 
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method")

    post = get_object_or_404(Post, post_id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    total = post.total_likes

    # redirect back
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)

@login_required
def logout_view(request):
    logout(request)
    return redirect('main_page')

@login_required(login_url='/')
@never_cache
def find_people_view(request):
    search_query = request.GET.get('search_user', '')
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if search_query:
        # Search for users whose first name, last name, or username contains the search query
        users = User.objects.filter(
            first_name__icontains=search_query
        ) | User.objects.filter(
            last_name__icontains=search_query
        ) | User.objects.filter(
            username__icontains=search_query
        )

    elif search_query == "":
        # Hide superusers
        users = User.objects.all().exclude(is_superuser=True)
    
    else:
        # If no search term is provided, retrieve all users
        users = User.objects.all()

    post_count = Post.objects.filter(user=user_profile.user).count()

    context = {
        'users' : users,
        'search_query' : search_query,
        'user_profile': user_profile,
        'post_count' : post_count,
    }

    return render(request, 'users/members.html', context)

@login_required
def user_posts_view(request, user_id):
    # get user by id
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    user = get_object_or_404(User, pk=user_id)

    # latest 5 posts
    posts = Post.objects.filter(user=user).order_by('-post_date')[:5]

    # get currently logged in user
    logged_in_user = request.user

    # when user is viewing his own profile
    is_own_profile = (logged_in_user.id == user_id)
    is_following = user_profile.following.filter(pk=request.user.pk).exists()
    follower_count = user_profile.following.count()
    post_count = Post.objects.filter(user=user_profile.user).count()

    context = {
        'user': user,
        'posts': posts,
        'user_profile' : user_profile,
        'is_own_profile' : is_own_profile,
        'post_count' : post_count,
        'logged_in_user': request.user,
        'is_following': is_following,
        'follower_count': follower_count,
    }

    return render(request, 'users/user_posts.html', context)

@login_required
def messages_view(request, u_id=None):
    # get all users except logged in user
    users = User.objects.exclude(id=request.user.id)
    # Hide superusers
    users = users.exclude(is_superuser=True)

    # get logged in user
    sender = request.user

    # get receiver
    if u_id:
        receiver = get_object_or_404(User, id=u_id)
        receiver_profile = get_object_or_404(UserProfile, user=receiver)
    else:
        receiver = None
        receiver_profile = None

    # fetch conversation
    if receiver:
        messages = Message.objects.filter(
            (models.Q(user_to=receiver) & models.Q(user_from=sender)) |
            (models.Q(user_from=receiver) & models.Q(user_to=sender))
        ).order_by('date')
    else:
        messages = []

    # Initialize error as None
    error = None

    # sending message
    if request.method == 'POST':
        msg_text = request.POST.get('msg_box')

        if not msg_text:
            error = "Message was unable to send!"
        elif len(msg_text) > 37:
            error = "Message is too long! Use only 37 characters."
        else:
            Message.objects.create(user_to=receiver, user_from=sender, msg_body=msg_text)
        
    user_profile = get_object_or_404(UserProfile, user=request.user)

    post_count = Post.objects.filter(user=user_profile.user).count()

    context = {
        'all_users': users,
        'messages' : messages,
        'user_to_msg' : receiver,
        'error' : error,
        'user_profile' : user_profile,
        'receiver_profile' : receiver_profile,
        'post_count' : post_count,
    }

    return render(request, 'users/messages.html', context)


@login_required(login_url='/')
def editProfile_view(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditUserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile has been updated successfully!')
            # Redirect to profile
            return redirect('profile', user_id=user.id)
        
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditUserProfileForm(instance=user_profile)

    post_count = Post.objects.filter(user=user_profile.user).count()

    context = {
            'user_form' : user_form,
            'profile_form' : profile_form,
            'user' : user,
            'user_profile' : user_profile,
            'post_count' : post_count,
        }
    
    return render(request, 'users/edit_profile.html', context)


@login_required
def myPosts_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    # Check if the logged-in user matches the profile user, If not, redirect to myposts with the logged-in user’s user_id.
    if request.user != user_profile.user:
        return redirect('myposts', user_id=request.user.id)

    posts = Post.objects.filter(user=user_profile.user).order_by('-post_date')

    post_count = posts.count()

    # when user is viewing his own post
    is_own_post = (request.user.id == user_id)

    context = {
        'user_profile' : user_profile,
        'posts' : posts,
        'is_own_post' : is_own_post,
        'post_count' : post_count,
    }

    return render(request, 'users/my_post.html', context)

@login_required
def post_search_view(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)

    query = request.GET.get('query')
    if query:
        results = Post.objects.filter(post_content__icontains=query)|Post.objects.filter(upload_image__icontains=query) 
    else:
        results = Post.objects.none()

    post_count = Post.objects.filter(user=user_profile.user).count()

    # when user is viewing his own post
    is_own_post = (request.user.id == user_id)

    # pagination
    per_page = 4 # results per page

    # Pagination logic
    paginator = Paginator(results, per_page) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'results':page_obj,  # Contains the paginated results
        'query' : query,
        'user_profile' : user_profile,
        'logged_in_user': request.user,
        'post_count': post_count, 
    }

    return render(request, 'users/results.html', context)

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email', '').strip().lower()
            recovery_answer = form.cleaned_data.get('recovery_answer', '')

            # Try to find the user with the given email and recovery answer

            try:
                user = User.objects.get(email=email, userprofile__recovery_answer=recovery_answer) # identify the user
                request.session['email'] = user.email # Store the email in session
                request.session['password_reset_allowed'] = True # Set permission for accessing the change password page
                return redirect('change_password')
            
            except User.DoesNotExist:
                # If the user is not found, display only this error message
                messages.error(request, "Your email or recovery answer is incorrect.")
               
        else:
             messages.error(request, "Form is not valid.")

    else:
        form = ForgotPasswordForm()
        
    return render(request, 'users/forgot_password.html', {'form':form})
    


def change_password_view(request):
    # Redirect to forgot password page if the session variable is not set
    if not request.session.get('password_reset_allowed'):
        messages.error(request, "Unauthorized access! Please fill this form")
        return redirect('forgot_password')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                if 6 <= len(password) <= 60:
                    email = request.session.get('email') # Get the email from session
                    
                    if email:
                        user = User.objects.get(email=email)
                        user.password = make_password(password)  # Hash the password
                        user.save()

                        # Clear the session variables after successful password reset
                        del request.session['password_reset_allowed']
                        del request.session['email']

                        messages.success(request, 'Your Password changed a moment ago!')
                        return redirect('login')  # Redirect to the login page
                    
                    else:
                        messages.error(request, "Session expired or invalid.")
                        return redirect('forgot_password')

                else:
                    messages.error(request, 'Your Password length must be between 6 - 60 characters!')

            else:
                messages.error(request, 'Your Passwords did not match!')

    else:
        form = ChangePasswordForm()

    return render(request, 'users/change_password.html', {'form': form})




def csrf_failure(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})



