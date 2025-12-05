from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from recipes.tests.helpers import reverse_with_next
from recipes.models import User, Recipe, Rating, Comment
from django.utils.timezone import make_aware
import datetime
from recipes.models import User, Recipe, Rating, RecipeIngredient, Unit, Ingredient, Comment
from recipes.views import getIngredients

class SpecificRecipeViewTestCase(TestCase):
    """Tests of the specific recipe view."""

    fixtures = ['recipes/tests/fixtures/default_user.json', 'recipes/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password='Password123')

        self.recipe = Recipe.objects.create(title="Test Recipe", description="desc", user=self.user)
        self.ingredient,_ = Ingredient.objects.get_or_create(name="Flour",user=self.user)
        self.unit,_ = Unit.objects.get_or_create(name="kgs",symbol="kgs",user=self.user)

        self.recipe_ingredient = RecipeIngredient.objects.create(
            user=self.user,
            recipe = self.recipe,
            ingredient = self.ingredient,
            unit = self.unit,
            quantity=2
        )


        self.url = reverse("get_recipe", args=[self.recipe.id])
        # add ratings
        Rating.objects.create(user=self.user, recipe=self.recipe, rating=4)
        Rating.objects.create(user=self.user2, recipe=self.recipe, rating=5)

    def test_view_loads_for_logged_in_user(self):
        """Page should load normally for logged-in users."""
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("recipe", response.context)


    def test_view_redirects_when_not_logged_in(self):
        """User must be logged in to access the view."""
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)

        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )
    def test_post_rating(self):
        """Test posting a rating for a recipe."""
        response = self.client.post(self.url, {'form_type': 'rating_form', 'rating': '5'})
        self.assertEqual(response.status_code, 302)

        rating = Rating.objects.get(user=self.user, recipe=self.recipe)
        self.assertEqual(rating.rating, 5)

    def test_invalid_rating(self):
        """Test posting an invalid rating."""
        response = self.client.post(self.url, {'form_type': 'rating_form', 'rating': 'invalid'})
        self.assertEqual(response.status_code, 302)

        rating = Rating.objects.get(user=self.user, recipe=self.recipe)
        self.assertEqual(rating.rating, 4)
    
    def test_average_rating_calculation(self):
        """Test if average rating is calculated correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        average_rating = response.context['average_rating']
        self.assertEqual(average_rating, 4.5) 
    
    def test_no_ratings(self):
        """Test view behavior when there are no ratings."""
        new_recipe = Recipe.objects.create(title="No Rating Recipe", description="desc", user=self.user)
        new_url = reverse("get_recipe", args=[new_recipe.id])

        response = self.client.get(new_url)
        self.assertEqual(response.status_code, 200)

        average_rating = response.context['average_rating']
        rating_count = response.context['rating_count']
        self.assertEqual(average_rating, 0) 
        self.assertEqual(rating_count, 0)    

    def test_post_rating_no_rating_value(self):
        """Test posting a rating with no value."""
        response = self.client.post(self.url, {'form_type': 'rating_form'})
        self.assertEqual(response.status_code, 302)

        rating = Rating.objects.get(user=self.user, recipe=self.recipe)
        self.assertEqual(rating.rating, 4)

    def test_post_out_of_bounds_rating(self):
        """Test posting an out-of-bounds rating."""
        response = self.client.post(self.url, {'form_type': 'rating_form', 'rating': '6'})
        self.assertEqual(response.status_code, 302)

        rating = Rating.objects.get(user=self.user, recipe=self.recipe)
        self.assertEqual(rating.rating, 4)

    def test_counting_recipe_comments(self):
        parent_comment = Comment.objects.create(user=self.user, comment="test comment", date_published=make_aware(datetime.datetime(2025,4,1)))
        self.recipe.comments.add(parent_comment)
        reply = Comment.objects.create(user=self.user, comment="test reply", date_published=make_aware(datetime.datetime(2025,1,1)))
        parent_comment.replies.add(reply)

        response = self.client.get(self.url)
        self.assertIn('recipe_comments_count', response.context)
        self.assertEqual(response.context['recipe_comments_count'], 2)
    def test_get_ingredients_returns_correct_list(self):
        result = getIngredients(self.recipe.id, multiplier=3)
        self.assertEqual(result,["6.00 kgs Flour"])
