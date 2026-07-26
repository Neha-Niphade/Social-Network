from django.db import models

class Tweet(models.Model):
    text = models.TextField()
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:30]