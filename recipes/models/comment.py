from django.db import models
from .user import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date_published = models.DateTimeField()
    
   