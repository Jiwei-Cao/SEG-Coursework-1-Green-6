from django.db import models
from .user import User

class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.TextField()

    def __str__(self):
        return self.name 