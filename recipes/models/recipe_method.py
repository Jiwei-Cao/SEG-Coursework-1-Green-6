from django.db import models
from .user import User
from .ingredient import Ingredient
from .unit import Unit
from .recipe import Recipe

class RecipeMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.TextField()
    order = models.IntegerField()

    def __str__(self):
        return str(self.recipe) + ": " + str(self.step) 