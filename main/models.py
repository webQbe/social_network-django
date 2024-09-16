from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    describe_user = models.CharField(max_length=255, default='Hello Coding Cafe. This is my default status!')
    relationship = models.CharField(max_length=100, blank=True)
    user_country = models.CharField(max_length=100)
    user_gender = models.CharField(max_length=10)
    user_birthday = models.DateField()
    user_image = models.ImageField(upload_to='profile_pics/', default='profile_pics/default_profile.png')
    user_cover = models.ImageField(upload_to='cover_pics/', default='cover_pics/default_cover.jpg')
    user_reg_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='verified')
    posts = models.TextField(default="0")
    recovery_answer = models.CharField(max_length=255,  default='Iwanttoputadingintheuniverse')

    def __str__(self):
        return self.user.username
