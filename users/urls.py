from django.urls import path
from . import views
from main.views import main_page
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('find/', views.find_view, name='find'),
    path('message/', views.message_view, name='message'),
    #path('myposts/<int:user_id>/', views.myPosts_view, name='my_posts'),
    #path('editprofile/<int:user_id>/', views.editProfile_view, name='edit_profile'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('search/', views.search_view, name='search_results'),
]
