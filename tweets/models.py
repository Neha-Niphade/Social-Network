from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    likes = models.ManyToManyField(
    User,
    related_name="liked_tweets",
    blank=True,
    )

    bookmarks = models.ManyToManyField(
    User,
    related_name="bookmarked_tweets",
    blank=True,
   )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text[:30]

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    tweet = models.ForeignKey(
        Tweet,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    text = models.TextField()
    
    likes = models.ManyToManyField(
    User,
    related_name="liked_comments",
    blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.text[:30]

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    message = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"