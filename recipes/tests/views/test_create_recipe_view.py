from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe
from recipes.forms import RecipeForm

class CreateRecipeViewTestCase(TestCase):
    """Tests of the create recipe view."""
    
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.url = reverse('create_recipe')
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.form_input = {
            'title': 'Pasta Bolognese',
            'description': 'A simple pasta recipe',
        }

    def test_create_recipe_url(self):
        self.assertEqual(self.url, '/create_recipe/')

    def test_get_create_recipe(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_get_create_recipe_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_recipe_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['title'] = ''
        before_count = Recipe.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())

    def test_successful_recipe_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Recipe.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        recipe = Recipe.objects.get(title=self.form_input['title'])
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(recipe.description, self.form_input['description'])

        expected_url = reverse('add_method', kwargs={'recipe_id': recipe.id})
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)