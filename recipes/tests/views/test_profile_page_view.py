from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe,Favourite
from recipes.tests.helpers import reverse_with_next
from math import floor

class ProfilePageViewTest(TestCase):
    """Test suite for the profile page View"""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.url = reverse('profile_page')
        self.user = User.objects.get(username='@johndoe')

    
    def test_profile_page_url(self):
        self.assertEqual(self.url, '/profile_page/')

    def test_get_profile_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_page.html')

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

        self.assertIn('full_stars', response.context)
        self.assertIn('half_star', response.context)
        self.assertIn('empty_stars', response.context)
        self.assertIn('recipes', response.context)

        rating = round(self.user.rating * 2) / 2
        full_stars = int(floor(rating))
        half_star = rating-full_stars==0.5
        empty_stars = 5 - full_stars - half_star
        self.assertEqual(range(full_stars), response.context['full_stars'])
        self.assertEqual(half_star, response.context['half_star'])
        self.assertEqual(range(empty_stars), response.context['empty_stars'])

        recipes = response.context['recipes']
        self.assertQuerySetEqual(recipes, Recipe.objects.filter(user=user))

    def test_get_profile_page_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_unfavourite_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        recipe = Recipe.objects.create(
            user=self.user,
            title="Test Recipe",
            description="Test Description",
            ingredients="Test Ingredients",
            method="Test Method"
        )
        
        Favourite.objects.create(user=self.user, recipe=recipe)

        form_input = {
            'form_type': 'favourite_form',
            'favourite_recipe': 'unfavourite_recipe',
            'recipe_clicked': str(recipe.id)
        }

        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Favourite.objects.filter(user=self.user, recipe=recipe).exists())