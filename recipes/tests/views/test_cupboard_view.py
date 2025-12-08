from django.test import TestCase
from django.urls import reverse
from recipes.models import User, UserIngredient, Unit
from recipes.forms import UserIngredientForm
from django.db import transaction

class CupboardPageViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_units.json',
        'recipes/tests/fixtures/default_user_ingredients.json',
        'recipes/tests/fixtures/default_tags.json'
    ]
    def setUp(self):
        self.url = reverse('cupboard')
        self.user = User.objects.get(username='@johndoe')
        self.unit = Unit.objects.get(name = 'tablespoon')
        self.user_ingredient= UserIngredient.objects.get(name='Tomato')
        self.form_input = {
            'name' : 'new ingredient',
            'category' : UserIngredient.BUTCHERY,
            'quantity' : 3,
            'unit' : Unit.objects.get(name='tablespoon').pk
        }

    
    def test_cupboard_page_url(self):
        self.assertEqual(self.url, '/cupboard/')

    def test_get_cupboard_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cupboard.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, UserIngredientForm))
        self.assertFalse(form.is_bound)
        self.ingredients_list = response.context.get('ingredients_list')
        self.ingredient = self.ingredients_list[0].get('ingredient')
        self.assertEqual(self.user_ingredient, self.ingredient)

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_ingredients_exists_in_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        ingredients = response.context.get('ingredients_list')
        self.assertIsNotNone(ingredients)
        self.assertTrue(len(ingredients) >= 0)

    def test_valid_form_saves(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)        
        before_count = UserIngredient.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserIngredient.objects.count()
        self.assertEqual(after_count, before_count + 1)
        expected_redirect_url = reverse("cupboard")
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_invalid_form_rejects(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)        
        self.form_input['quantity'] = 'five'
        before_count = UserIngredient.objects.count()
        with transaction.atomic():
            response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserIngredient.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cupboard.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, UserIngredientForm))
        self.assertFalse(form.is_bound)

