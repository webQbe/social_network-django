from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm
from .models import UserProfile

# Create your views here.

def main_page(request):
    return render(request, 'main/main.html')

def signup_view(request):
    return render(request, 'main/register.html')

def loginform_view(request):
    return render(request, 'main/login.html')
    
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        # find the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None


        # Authenticate the user
        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')  # Redirect to home page after successful login
                else:
                    messages.error(request, 'Account is disabled.')
            else:
                messages.error(request, 'Your email or password is incorrect!')
        else:
            messages.error(request, 'Your email or password is incorrect!')

    return render(request, 'main/login.html')

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
      
            # Create a new user with only the username and password first
            user = User.objects.create_user(
                username=f"{form.cleaned_data['first_name'].lower()}_{form.cleaned_data['last_name'].lower()}_{str(User.objects.count() + 1).zfill(5)}",
                password=form.cleaned_data['u_pass'],
            )
            # Now assign the other fields
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['u_email']
            user.save()
           

            # Assign a random profile image
            user_image = f'head_{["red", "sunflower", "turquoise"][User.objects.count() % 3]}.png'

            # Create the UserProfile with the user instance
            profile = UserProfile.objects.create(
                user=user,
                user_image=user_image,
                user_birthday=form.cleaned_data['u_birthday'],
                user_country=form.cleaned_data['u_country'],
                user_gender=form.cleaned_data['u_gender'],
            )
            profile.save()

            # redirect to login page after successful registration 
            return redirect('login')  
        
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form':form})


