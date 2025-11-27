"""Tests for the edit_recipe view."""
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm
from recipes.models import User, Recipe
from recipes.tests.helpers import reverse_with_next

class EditRecipeViewTest(TestCase):
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
        
        self.url = reverse('edit_recipe', args=[self.recipe.id])
        self.client.login(username=self.user.username, password="Password123")
    
    def test_recipe_owner_can_edit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_unauthorised_user_cannot_edit(self):
        self.client.logout()

        user2 = User.objects.create(username="@janedoe", email="janedoe@example.com")
        user2.set_password("Password123")
        user2.save()
        self.client.login(username=user2.username, password="Password123")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_edit_page_renders_with_recipe_data(self):
        response = self.client.get(self.url)

        self.assertContains(response, self.recipe.title)
        self.assertContains(response, self.recipe.description)

        self.assertTemplateUsed('edit_recipe.html')
    
    def test_edit_recipe_success(self):
        new_title = 'new title'
        data = {
            'title': new_title,
            'description': self.recipe.description,
            'tags':[]
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code,302)
        expected_url = reverse('get_recipe', args=[self.recipe.id])
        self.assertRedirects(response, expected_url)

        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, new_title)

    def test_edit_recipe_with_invalid_form(self):
        data = {
            'title':''
        }
        response = self.client.post(self.url, data)
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertIn('This field is required.', form.errors['title'])
        

    def test_edit_recipe_redirects_when_not_logged_in(self):
        self.client.logout()
        response = self.client.get(self.url)
        expected_url = reverse_with_next('log_in', self.url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_get_edit_recipe_with_nonexistent_recipe(self):
        url = reverse('edit_recipe', args=[self.recipe.id + 1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_edit_recipe_with_nonexistent_recipe(self):
        url = reverse('edit_recipe', args=[self.recipe.id + 1])
        data = {
            'title': 'new_title',
            'description': self.recipe.description,
            'tags':[]
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
