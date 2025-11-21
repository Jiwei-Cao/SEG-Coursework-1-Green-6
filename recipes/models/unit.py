from django.db import models
from .user import User

class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol 