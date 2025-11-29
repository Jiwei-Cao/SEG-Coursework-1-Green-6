from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Rating
from recipes.views.dashboard_view import star_rating

class DashBoardViewTestCase(TestCase):
    """Tests of the dashboard view."""

    fixtures = ['recipes/tests/fixtures/default_user.json', 'recipes/tests/fixtures/other_users.json']

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')
        self.client.login(username=self.user.username, password='Password123')

        # create recipes
        self.recipe1 = Recipe.objects.create(title="R1", description="desc",  user=self.user)
        self.recipe2 = Recipe.objects.create(title="R2", description="desc", user=self.user)
        self.recipe3 = Recipe.objects.create(title="R3", description="desc", user=self.user)
        self.recipe4 = Recipe.objects.create(title="R4", description="desc",  user=self.user)
        self.recipe5 = Recipe.objects.create(title="R5", description="desc", user=self.user)

        # add ratings
        Rating.objects.create(user=self.user, recipe=self.recipe1, rating=5)
        Rating.objects.create(user=self.user2, recipe=self.recipe1, rating=3)

        Rating.objects.create(user=self.user, recipe=self.recipe2, rating=4)
        Rating.objects.create(user=self.user, recipe=self.recipe3, rating=2)

        Rating.objects.create(user=self.user2, recipe=self.recipe4, rating=5)

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_get_dashboard_no_login_redirects(self):
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        login_url = reverse('log_in') + '?next=' + self.url
        self.assertRedirects(response, login_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'log_in.html')

    def test_average_rating_and_sorting(self):
        recipes = Recipe.objects.all()

        rated_recipes = sorted(
        recipes,
        key=lambda r: (r.average_rating, r.rating_count, -r.id),
        reverse=True
    )[:4]

        # check top recipe
        self.assertEqual(rated_recipes[0], self.recipe4)  
        self.assertEqual(rated_recipes[1], self.recipe1) 
        self.assertEqual(rated_recipes[2], self.recipe2)  
        self.assertEqual(rated_recipes[3], self.recipe3)  

        # check average_rating and rating_count
        self.assertEqual(self.recipe1.average_rating, 4.0)
        self.assertEqual(self.recipe1.rating_count, 2)
        self.assertEqual(self.recipe2.average_rating, 4.0)
        self.assertEqual(self.recipe2.rating_count, 1)
        self.assertEqual(self.recipe3.average_rating, 2.0)
        self.assertEqual(self.recipe3.rating_count, 1)
        self.assertEqual(self.recipe4.average_rating, 5)
        self.assertEqual(self.recipe4.rating_count, 1)
        self.assertEqual(self.recipe5.average_rating, 0)
        self.assertEqual(self.recipe5.rating_count, 0)

    def test_star_rating_adds_dynamic_attributes(self):
        """Before calling star_rating(), attributes shouldn't exist."""
        self.assertFalse(hasattr(self.recipe5, "full_stars"))
        self.assertFalse(hasattr(self.recipe5, "half_stars"))
        self.assertFalse(hasattr(self.recipe5, "empty_stars"))

        # apply star rating logic
        star_rating(self.recipe5)

        """After calling star_rating(), attributes are created."""
        self.assertTrue(hasattr(self.recipe5, "full_stars"))
        self.assertTrue(hasattr(self.recipe5, "half_stars"))
        self.assertTrue(hasattr(self.recipe5, "empty_stars"))

    def test_star_rating_zero(self):
        star_rating(self.recipe5)

        self.assertEqual(len(self.recipe5.full_stars),0)
        self.assertEqual(self.recipe5.half_stars, 0)
        self.assertEqual(len(self.recipe5.empty_stars),5)

    def test_star_rating_full_star(self):
        Rating.objects.create(user = self.user, recipe=self.recipe5, rating=4)

        star_rating(self.recipe5)

        self.assertEqual(len(self.recipe5.full_stars),4)
        self.assertEqual(self.recipe5.half_stars, 0)
        self.assertEqual(len(self.recipe5.empty_stars),1)

    def test_star_rating_half_star(self):
        Rating.objects.create(user = self.user, recipe=self.recipe5, rating=4)
        Rating.objects.create(user = self.user2, recipe=self.recipe5, rating=3)

        star_rating(self.recipe5)

        self.assertEqual(len(self.recipe5.full_stars),3)
        self.assertEqual(self.recipe5.half_stars, 1)
        self.assertEqual(len(self.recipe5.empty_stars),1)

    def test_star_rating_round_off(self):
        Rating.objects.create(user = self.user, recipe=self.recipe5, rating=4)
        Rating.objects.create(user = self.user2, recipe=self.recipe5, rating=5)
        Rating.objects.create(user = self.user3, recipe=self.recipe5, rating=4)

        star_rating(self.recipe5)

        self.assertEqual(len(self.recipe5.full_stars),4)
        self.assertEqual(self.recipe5.half_stars, 0)
        self.assertEqual(len(self.recipe5.empty_stars),1)

    