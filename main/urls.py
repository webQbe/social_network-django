from django.urls import path
#from .views import main_page, SignupView, LoginView  # Assuming you have these views
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
]
