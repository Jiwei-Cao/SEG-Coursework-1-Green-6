from recipes.models import User, Tag, Ingredient, RecipeIngredient, Unit
from django.test import TestCase
from django.core.exceptions import ValidationError

class RecipeIngredientModelTestCase(TestCase):
    """Unit tests for the Recipe model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_units.json',
        'recipes/tests/fixtures/default_recipe.json',
        'recipes/tests/fixtures/default_ingredients.json',
        'recipes/tests/fixtures/default_recipe_ingredients.json'
    ]

    def setUp(self):
        self.recipeingredient = RecipeIngredient.objects.get(pk=1)

    def test_valid_recipeingredient(self):
        self._assert_recipeingredient_is_valid()

    def test_user_must_not_be_blank(self):
        self.recipeingredient.user = None
        self._assert_recipeingredient_is_invalid()

    def test_recipe_must_not_be_blank(self):
        self.recipeingredient.recipe = None
        self._assert_recipeingredient_is_invalid()

    def test_quantity_must_not_be_blank(self):
        self.recipeingredient.quantity = None
        self._assert_recipeingredient_is_invalid()

    def test_ingredient_must_not_be_blank(self):
        self.recipeingredient.ingredient = None
        self._assert_recipeingredient_is_invalid()

    def test_unit_must_not_be_blank(self):
        self.recipeingredient.unit = None
        self._assert_recipeingredient_is_invalid()

    def test_str_returns_line_desc(self):
        self.expected_line = "5.00 kgs of Tomato"
        self.assertEqual(str(self.recipeingredient), self.expected_line)

    def _assert_recipeingredient_is_valid(self):
        try:
            self.recipeingredient.full_clean()
        except ValidationError:
            self.fail('Test recipe ingredient should be valid')

    def _assert_recipeingredient_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipeingredient.full_clean()
