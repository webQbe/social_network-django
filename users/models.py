from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(blank=True, null=True)
    upload_image = models.ImageField(upload_to='imagepost/', blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Ensure post_content is not None
        post_content_preview = self.post_content[:20] if self.post_content else ""
        return f'{self.user.username} - {post_content_preview}'
