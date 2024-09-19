from django.urls import path
from . import views
from main.views import main_page
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler403

urlpatterns = [
    #path('recovery/<int:user_profile_id>/', views.recovery_view, name='recovery'),
    path('edit_profile/', views.editProfile_view, name='edit_profile'),
    path('messages/<int:u_id>/', views.messages_view, name='messages'),
    path('user_profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('find_people/', views.find_people_view, name="find_people"),
    path('post/<int:post_id>/comment/', views.comment_post_view, name='comment_post'),
    path('post/<int:post_id>/', views.single_post_view, name='single_post'),
    path('post/<int:post_id>/edit', views.edit_post_view, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete_profile, name='p_post_delete'),  
    path('post/<int:post_id>/delete/', views.post_delete_home, name='h_post_delete'), 
    path('post/new/', views.create_post_view, name="create_post"), 
    path('update_profile/<int:user_id>/', views.updateProfileImage_view , name="update_image"),
    path('update_cover/<int:user_id>/', views.updateCover_view, name="update_cover"),
    path('home/', views.home_view, name='home'),
    path('profile/<int:user_id>/', views.profile_view, name='profile'),
    path('logout/', views.logout_view, name='logout'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = 'yourapp.views.csrf_failure'