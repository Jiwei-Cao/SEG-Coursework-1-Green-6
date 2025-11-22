from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Ingredient

class CupboardPageViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.url = reverse('cupboard')
        self.user = User.objects.get(username='@johndoe')
        self.ingredient1 = Ingredient.objects.create(
            name="fish",
            category= Ingredient.SEAFOOD,
            user=self.user
        )
        self.ingredient2 = Ingredient.objects.create(
            name="paprika",
            category = Ingredient.SPICE,
            user=self.user
        )

    
    def test_cupboard_page_url(self):
        self.assertEqual(self.url, '/cupboard/')

    def test_get_cupboard_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cupboard.html')
        self.assertIn(self.ingredient1, response.context['ingredients'])
        self.assertIn(self.ingredient2, response.context['ingredients'])

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_ingredients_exists_in_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        ingredients = response.context.get('ingredients')
        self.assertIsNotNone(ingredients)
        self.assertTrue(len(ingredients) >= 0)