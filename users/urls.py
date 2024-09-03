from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
]
