from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView as AuthLoginView

# Create your views here.

def main_page(request):
    return render(request, 'main.html')

def signup_view(request):
    return render(request, 'signup.html')
    
def login_view(request):
    return render(request, 'login.html')
