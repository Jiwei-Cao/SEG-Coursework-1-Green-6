from django.test import TestCase
from django.urls import reverse
from recipes.tests.helpers import reverse_with_next
from recipes.models import User, Recipe, Rating

class ToggleFavouriteViewTestCase(TestCase):
    """Tests of the toggle_favourite view"""

    def setUp(self):
        self.user = User.objects.create(username="@johndoe")
        self.user.set_password("Password123")
        self.user.save()
        self.recipe_data = {
            "user": self.user,
            "title": "Tomato Soup",
            "description": "Basic soup",
        }
        self.recipe = Recipe.objects.create(
            user = self.recipe_data['user'],
            title = self.recipe_data['title'],
            description = self.recipe_data['description'],
        )

        self.url = reverse('toggle_favourite', args=[self.recipe.id])
        self.client.login(username="@johndoe", password="Password123")
    
    def test_toggle_favourite_url(self):
        self.assertEqual(self.url, f'/recipe/{self.recipe.id}/toggle_favourite')

    def test_toggle_favourite_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        expected_url = reverse_with_next('log_in',self.url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_redirect_fallback(self):
        response = self.client.post(self.url, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'recipe/{self.recipe.id}')

    def test_get_toggle_favourite_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_post_toggle_favourite_adds_user(self):
        response = self.client.post(self.url)
        self.assertIn(self.user, self.recipe.favourites.all())
        self.assertEqual(response.status_code, 302)

    def test_post_toggle_favourite_removes_user(self):
        self.recipe.favourites.add(self.user)
        response = self.client.post(self.url)
        self.assertNotIn(self.user, self.recipe.favourites.all())
        self.assertEqual(response.status_code, 302)
    
    def test_post_toggle_favourite_with_invalid_recipe_id(self):
        url = reverse('toggle_favourite', args=[self.recipe.id + 1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_to_referer(self):
        referer = '/all_recipes/'
        response = self.client.post(self.url, HTTP_REFERER=referer)
        self.assertRedirects(response, referer)