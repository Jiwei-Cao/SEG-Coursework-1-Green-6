from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe
from recipes.tests.helpers import reverse_with_next
from math import floor
from django.http import Http404

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

    def test_profile_page_fetch_other_user(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(reverse("profile_page", args=[self.user2.username]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["user"], self.user2)
        self.assertTemplateUsed(response, 'profile_page.html')


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