from django.db import models
from .user import User
from .recipe import Recipe

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'recipe')