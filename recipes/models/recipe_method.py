from django.db import models
from .user import User
from .recipe import Recipe

class RecipeMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.TextField()
    order = models.IntegerField() 

    class Meta:
        unique_together = ["recipe", "order"]

    def __str__(self):
        return str(self.recipe) + ": " + str(self.order) + " " + str(self.step)