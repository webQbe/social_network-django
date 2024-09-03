from django.urls import path
from . import views
from users.views import register_view

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('signup/', register_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('loginform/', views.loginform_view, name='loginform'),
    path('home/', views.home_view, name='home'),
]
