from django.contrib import admin
from main.models import UserProfile
from .models import Post, Comment, Message

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Message)