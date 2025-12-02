from django.db import models
from .user import User
from .ingredient import Ingredient
from .unit import Unit
from .recipe import Recipe

class RecipeIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits= 10)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recipe.update_tags()

    def delete(self, *args, **kwargs):
        recipe = self.recipe
        super().delete(*args, **kwargs)
        recipe.update_tags()

    def __str__(self):
        return str(self.recipe) + ": " + str(self.quantity) + " " + str(self.unit) + " of " + str(self.ingredient) 