from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('loginform/', views.loginform_view, name='loginform'),
]
