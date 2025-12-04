"""Unit tests for the Recipe model."""

from recipes.models import Recipe, User, Rating
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

    def test_title_may_contain_100_characters(self):
        self.recipe.title = 'x' * 100
        self._assert_recipe_is_valid()

    def test_title_must_not_contain_more_than_100_characters(self):
        self.recipe.title = 'x' * 101
        self._assert_recipe_is_invalid()

    def test_description_must_not_be_blank(self):
        self.recipe.description = ''
        self._assert_recipe_is_invalid()

    def test_ingredients_can_be_blank(self):
        self.recipe.ingredients = ''
        self._assert_recipe_is_valid()

    def test_method_can_be_blank(self):
        self.recipe.method = ''
        self._assert_recipe_is_valid()

    def test_str_returns_title(self):
        self.recipe.title = "My Recipe Title"
        self.assertEqual(str(self.recipe), "My Recipe Title")

    def test_user_can_add_favourite_recipe(self):
        user = User.objects.create(username="@Janedoe")
        self.recipe.favourites.add(user)
        self.assertIn(user, self.recipe.favourites.all())

    def test_user_can_unfavourite_recipe(self):
        user = User.objects.create(username="@Janedoe")
        self.recipe.favourites.add(user)
        self.assertIn(user, self.recipe.favourites.all())
        self.recipe.favourites.remove(user)
        self.assertNotIn(user, self.recipe.favourites.all())

    def test_no_rating_returns_zero(self):
        self.assertFalse(self.recipe.rating_set.exists())
        self.assertEqual(self.recipe.average_rating,0)

    def test_average_calculated_correctly(self):
        user = User.objects.create(username="@Janedoe", email="janedoe@example.com")
        user1 = User.objects.create(username="@Happy", email="happy@example.com")
        Rating.objects.create(user=user, recipe=self.recipe, rating=4)
        Rating.objects.create(user=user1, recipe=self.recipe, rating=2)

        self.assertTrue(self.recipe.rating_set.exists())
        self.assertAlmostEqual(self.recipe.average_rating, 3.0)


    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except ValidationError:
            self.fail('Test recipe should be valid')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
