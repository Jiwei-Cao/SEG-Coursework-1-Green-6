from django.test import TestCase
from django.urls import reverse
from recipes.models import User, UserIngredient, Unit

class CupboardPageViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_units.json',
        'recipes/tests/fixtures/default_user_ingredients.json'
    ]
    def setUp(self):
        self.url = reverse('cupboard')
        self.user = User.objects.get(username='@johndoe')
        self.unit = Unit.objects.get(name = 'tablespoon')
        self.user_ingredient= UserIngredient.objects.get(name='Tomato')

    
    def test_cupboard_page_url(self):
        self.assertEqual(self.url, '/cupboard/')

    def test_get_cupboard_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cupboard.html')
        self.ingredients_list = response.context.get('ingredients_list')
        self.ingredient = self.ingredients_list[0].get('ingredient')
        self.assertEqual(self.user_ingredient, self.ingredient)

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_ingredients_exists_in_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        ingredients = response.context.get('ingredients_list')
        self.assertIsNotNone(ingredients)
        self.assertTrue(len(ingredients) >= 0)