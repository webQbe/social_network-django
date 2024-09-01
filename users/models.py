from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=150, unique=True)
    describe_user = models.CharField(max_length=255, blank=True)
    relationship = models.CharField(max_length=100, blank=True)
    user_pass = models.CharField(max_length=255)
    user_email = models.EmailField(max_length=255, unique=True)
    user_country = models.CharField(max_length=100)
    user_gender = models.CharField(max_length=10)
    user_birthday = models.DateField()
    user_image = models.ImageField(upload_to='profile_pics/', blank=True)
    user_cover = models.ImageField(upload_to='cover_pics/', blank=True)
    user_reg_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, blank=True)
    posts = models.IntegerField(default=0)
    recovery_account = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user_name
