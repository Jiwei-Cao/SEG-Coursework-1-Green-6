from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Ingredient
from recipes.forms import IngredientForm
from django.db import transaction

class CreateIngredientViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_ingredients.json',
    ]
    def setUp(self):
        self.url = reverse('specify_ingredient')
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'name' : 'New Ingredient',
            'category' : Ingredient.BUTCHERY,
        }

    
    def test_specify_ingredient_url(self):
        self.assertEqual(self.url, '/manage_recipe_ingredient/specify_ingredient/')

    def test_get_specify_ingredient_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specify_ingredient.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, IngredientForm))
        self.assertFalse(form.is_bound)

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_valid_form_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)        
        before_count = Ingredient.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Ingredient.objects.count()
        self.assertEqual(after_count, before_count + 1)
        expected_redirect_url = reverse("specify_ingredient")
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_invalid_form_rejects(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)        
        self.form_input['category'] = 5
        before_count = Ingredient.objects.count()
        with transaction.atomic():
            response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Ingredient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specify_ingredient.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, IngredientForm))
        self.assertTrue(form.is_bound)