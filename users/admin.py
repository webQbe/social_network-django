from django.contrib import admin
from main.models import UserProfile
from .models import Post
from .models import Comment

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)