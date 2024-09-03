from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View

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

@login_required
def home_view(request):
    return render(request, 'main/home.html')