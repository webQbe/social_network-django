from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.CharField(max_length=250, blank=True)
    upload_image = models.ImageField(upload_to='imagepost/', blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.post_content[:20]}'
