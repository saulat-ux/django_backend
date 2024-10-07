from django.db import models
from django.contrib.auth.models import User

class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who created the post
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
