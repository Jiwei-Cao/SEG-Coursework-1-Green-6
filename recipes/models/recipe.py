from django.db import models
from .user import User
from .tag import Tag

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    method = models.TextField()
    img = models.ImageField(upload_to='images/', blank=True, default='images/default.webp')
    tags = models.ManyToManyField(Tag,blank=True)

    def __str__(self):
        return self.title 