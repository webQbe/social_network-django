from django.contrib import admin
from main.models import UserProfile
from .models import Post, Comment, Message

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Message)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user', 'post_date', 'total_likes')