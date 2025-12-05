from django.db import models
from .user import User

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(blank=False, max_length=500)
    date_published = models.DateTimeField()
    
    replies = models.ManyToManyField("self", symmetrical=False, blank=True, related_name='comment_replies')
   
    class Meta:
        ordering = ('date_published',)