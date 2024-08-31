from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView as AuthLoginView

# Create your views here.

def main_page(request):
    return render(request, 'main/main.html')

class SignupView(View):
    def get(self, request):
        # Your signup logic
        return render(request, 'signup.html')
    
class LoginView(AuthLoginView):
    template_name = 'login.html'
