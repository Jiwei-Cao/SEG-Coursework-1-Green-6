from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Rating
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
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username="@petrapickles")

        self.user.following.add(self.user2)
        self.user2.following.add(self.user3)

    
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

    def test_profile_page_with_no_recipes(self):
        self.client.login(username=self.user3.username, password="Password123")

        url = reverse("profile_page", args=[self.user3.username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["rating_count"],0)
        self.assertEqual(self.user3.rating,0)

    def test_profile_page_rating_calculation(self):
        self.client.login(username=self.user.username, password='Password123')

        recipe1 = Recipe.objects.create(title="R1", description= "smth", created_at="2025-11-21T12:00:00Z", user=self.user)
        recipe2 = Recipe.objects.create(title="R2", description= "smth", created_at="2025-11-21T12:00:00Z", user=self.user)
        Rating.objects.create(recipe=recipe1, user=self.user2, rating=4)
        Rating.objects.create(recipe=recipe1, user=self.user3, rating=2)
        Rating.objects.create(recipe=recipe2, user=self.user2, rating=5)

        response = self.client.get(self.url)

        expected_rating = (4 + 2 + 5) / 3
        profile_user = response.context["user"]
        self.assertAlmostEqual(profile_user.rating, expected_rating, places=2)

        self.assertEqual(response.context["rating_count"], 3)
    
    def test_star_rating_rounding(self):
        self.client.login(username=self.user.username, password='Password123')

        recipe = Recipe.objects.create(user=self.user, title="R",description= "smth", created_at="2025-11-21T12:00:00Z")

        Rating.objects.create(recipe=recipe, rating=3.24, user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(len(response.context["full_stars"]), 3)
        self.assertFalse(response.context["half_star"])

    def test_profile_page_fetch_other_user(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(reverse("profile_page", args=[self.user2.username]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user2)
        self.assertTemplateUsed(response, 'profile_page.html')

    def test_most_popular_is_none_when_no_recipes(self):
        self.client.login(username=self.user3.username, password='Password123')

        url = reverse("profile_page", args=[self.user3.username])
        response = self.client.get(url)

        self.assertIsNone(response.context["most_popular"])

    def test_most_favourite_is_none_when_no_recipes(self):
        self.client.login(username=self.user3.username, password='Password123')

        url = reverse("profile_page", args=[self.user3.username])
        response = self.client.get(url)
        self.assertIsNone(response.context["most_favourite"])

    def test_most_popular_recipe(self):
        self.client.login(username=self.user.username, password="Password123")

        recipe1 = Recipe.objects.create(user=self.user, title="recipe1",description= "smth", created_at="2025-11-21T12:00:00Z")
        recipe2 = Recipe.objects.create(user=self.user, title="recipe2",description= "smth", created_at="2025-11-21T12:00:00Z")

        Rating.objects.create(recipe=recipe1, rating=2, user=self.user2)
        Rating.objects.create(recipe=recipe2, rating=5, user=self.user2)

        response = self.client.get(self.url)
        self.assertEqual(response.context['most_popular'], recipe2.id)

    def test_most_favourite_recipe(self):
        self.client.login(username=self.user.username, password="Password123")

        recipe1 = Recipe.objects.create(user=self.user, title="recipe1",description= "smth", created_at="2025-11-21T12:00:00Z")
        recipe2 = Recipe.objects.create(user=self.user, title="recipe2",description= "smth", created_at="2025-11-21T12:00:00Z")

        recipe1.favourites.add(self.user2)
        recipe2.favourites.add(self.user2, self.user3)

        response = self.client.get(self.url)
        self.assertEqual(response.context["most_favourite"], recipe2.id)

    def test_most_favourite_tie_created_at(self):
        """When have two most favourited recipes, the newest recipe should be the most favourited one"""
        self.client.login(username=self.user.username, password='Password123')

        recipe1 = Recipe.objects.create(title="Old", description= "smth",user=self.user, created_at="2020-11-21T12:00:00Z")
        recipe2 = Recipe.objects.create(title="New",description= "smth", user=self.user, created_at="2025-11-21T12:00:00Z")

        recipe1.favourites.add(self.user2)
        recipe2.favourites.add(self.user3)

        recipe1.save()

        response = self.client.get(self.url)
        self.assertEqual(response.context["most_favourite"], recipe2.id)

    def test_user_cannot_follow_themselves(self):
        self.client.login(username=self.user.username, password="Password123")

        response = self.client.get(self.url)
        self.assertFalse(response.context["is_following"])

    def test_following_list(self):
        self.client.login(username=self.user.username, password="Password123")

        url = reverse("following_list", args = [self.user.username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

        self.assertEqual(response.context["profile_user"], self.user)
        self.assertEqual(list(response.context['users']), list(self.user.following.all()))
        self.assertIn(self.user2.id, response.context["following_ids"])

    def test_followers_list(self):
        self.client.login(username=self.user2.username, password="Password123")
        url = reverse('followers_list', args = [self.user2.username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')

        self.assertEqual(response.context['profile_user'], self.user2)
        self.assertEqual(list(response.context['users']), list(self.user2.followers.all()))
        
        following_ids = response.context['following_ids']
        self.assertIsInstance(following_ids, set)
        self.assertIn(self.user3.id, following_ids)

    def test_following_list_404_for_non_existent_user(self):
        self.client.login(username=self.user.username, password = "Password123")
        url = reverse('following_list', args = ["non_existent"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_followers_list_404_for_non_existent_user(self):
        self.client.login(username=self.user.username, password = "Password123")
        url = reverse('followers_list', args = ["non_existent"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_profile_page_is_following_for_other_user(self):
        self.client.login(username= self.user.username, password = "Password123")

        self.user.following.add(self.user3)

        url = reverse('profile_page', args = [self.user3.username])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile_page.html")

        self.assertTrue(response.context['is_following'])