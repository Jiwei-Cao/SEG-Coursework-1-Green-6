"""Unit tests for the Recipe model."""

from recipes.models import Recipe, User 
from django.test import TestCase
from django.core.exceptions import ValidationError

class RecipeModelTestCase(TestCase):
    """Unit tests for the Recipe model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/default_recipe.json'
    ]

    def setUp(self):
        self.recipe = Recipe.objects.get(pk=1)

    def test_valid_recipe(self):
        self._assert_recipe_is_valid()

    def test_user_must_not_be_blank(self):
        self.recipe.user = None
        self._assert_recipe_is_invalid()

    def test_title_must_not_be_blank(self):
        self.recipe.title = ''
        self._assert_recipe_is_invalid()

    

    
    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test recipe should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
