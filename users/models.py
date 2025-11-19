from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_content = models.TextField(blank=True, null=True)
    upload_image = models.ImageField(upload_to='imagepost/', blank=True, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        # Ensure post_content is not None
        post_content_preview = self.post_content[:20] if self.post_content else ""
        return f'{self.user.username} - {post_content_preview}'
    
    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    # Primary key com_id will be auto-created as id field by default
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, max_length=255)
    comment_author = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Ensure comment is not None
        comment_preview = self.comment[:20] if self.comment else ""
        return f'{self.comment_author} - {comment_preview}'


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    user_to = models.ForeignKey(User, related_name='messages_received', on_delete=models.CASCADE)
    user_from = models.ForeignKey(User, related_name='messages_sent', on_delete=models.CASCADE)
    msg_body = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    msg_seen = models.CharField(max_length=10)

    def __str__(self):
        return f'Message from {self.user_from} to {self.user_to}'