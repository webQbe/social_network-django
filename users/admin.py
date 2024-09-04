from django.contrib import admin
from main.models import UserProfile
from .models import Post

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)