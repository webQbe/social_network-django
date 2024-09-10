from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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


class Comment(models.Model):
    # Primary key com_id will be auto-created as id field by default
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_author = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Ensure comment is not None
        comment_preview = self.comment[:20] if self.comment else ""
        return f'{self.comment_author} - {comment_preview}'