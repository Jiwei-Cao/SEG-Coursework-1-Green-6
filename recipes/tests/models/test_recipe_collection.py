"""Unit tests for the Recipe model."""

from recipes.models import Recipe, RecipeIngredient, RecipeMethod
from django.test import TestCase
from django.core.exceptions import ValidationError

class RecipeModelTestCase(TestCase):
    """Unit tests for the Recipe model."""

    def setUp(self):
        self.recipes = Recipe.objects.get()
        self.recipeIngredients = RecipeIngredient.objects.get()
        self.recipeMethods = RecipeMethod.objects.get()
