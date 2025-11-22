from django.test import TestCase
from django.urls import reverse
from recipes.tests.helpers import reverse_with_next
from recipes.models import User, Recipe

class DeleteRecipeViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="@johndoe")
        self.user.set_password("Password123")
        self.user.save()
        self.recipe_data = {
            "user": self.user,
            "title": "Tomato Soup",
            "description": "Basic soup",
            "ingredients": "Tomatoes\nSalt\nWater",
            "method": "Boil tomatoes.\nBlend.\nServe."
        }
        self.recipe = Recipe.objects.create(
            user = self.recipe_data['user'],
            title = self.recipe_data['title'],
            description = self.recipe_data['description'],
            ingredients = self.recipe_data['ingredients'],
            method = self.recipe_data['method']
        )

        self.url = reverse('delete_recipe', args=[self.recipe.id])
        self.client.login(username="@johndoe", password="Password123")
    
    def test_delete_recipe_url(self):
        self.assertEqual(self.url, f"/recipe/{self.recipe.id}/delete")

    def test_get_delete_recipe_request_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_delete_recipe_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        expected_url = reverse_with_next('log_in',self.url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
    
    def test_delete_recipe_with_invalid_id(self):
        url = reverse('delete_recipe', args=[self.recipe.id + 1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
    
    def test_valid_delete_recipe_request(self):
        recipe_id = self.recipe.id
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Recipe.objects.filter(id=recipe_id).exists())
    
    def test_delete_recipe_redirects_to_dashboard(self):
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('dashboard'))

    def test_unauthorised_user_delete_request_rejects(self):
        self.client.logout()

        user2 = User.objects.create(username="@Janedoe", email="janedoe@example.com")
        user2.set_password("Password123")
        user2.save()

        self.client.login(username="@Janedoe", password="Password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)