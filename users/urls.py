from django.urls import path
from . import views
from main.views import main_page
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403

urlpatterns = [
    path('posts', views.get_posts_view, name="posts"),  
    path('post/new/', views.create_post_view, name="create_post"), 
    path('update_profile/<int:user_id>/', views.updateProfileImage_view , name="update_image"),
    path('update_cover/<int:user_id>/', views.updateCover_view, name="update_cover"),
    path('home/', views.home_view, name='home'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('find/', views.find_view, name='find'),
    path('message/', views.message_view, name='message'),
    #path('myposts/<int:user_id>/', views.myPosts_view, name='my_posts'),
    #path('editprofile/<int:user_id>/', views.editProfile_view, name='edit_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search_results'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'yourapp.views.csrf_failure'