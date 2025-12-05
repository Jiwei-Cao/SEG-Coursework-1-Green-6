from django.test import TestCase
from django.urls import reverse
from recipes.tests.helpers import reverse_with_next
from recipes.models import User
from recipes.views import get_follower_summary

class UserSearchViewTestCase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user1 = User.objects.get(username='@janedoe')
        self.user2 = User.objects.get(username='@picklepeters')

        self.client.login(username=self.user.username, password='Password123')
        self.url = reverse("user_search")

        self.user1.followers.add(self.user2)

    def test_user_search_view_when_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIn("users", response.context)
        self.assertIn("top_users", response.context)
        self.assertIn("following_ids", response.context)

    def test_redirect_when_not_logged_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)

        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_search_filter_user(self):
        response = self.client.get(self.url + "?q=jane")
        users = response.context["users"]

        self.assertIn(self.user1, users)
        self.assertNotIn(self.user, users)

    def test_no_query_return_all_other_users(self):
        response = self.client.get(self.url)
        users = response.context["users"]

        self.assertIn(self.user1, users)
        self.assertIn(self.user2, users)

    def test_top_users_sort_by_follower_count(self):
        response = self.client.get(self.url)
        top_users = list(response.context["top_users"])

        self.assertGreaterEqual(len(top_users),2)
        self.assertEqual(top_users[0], self.user1)
    
    def test_following_id_exists(self):
        self.user.following.add(self.user1)

        response = self.client.get(self.url)
        following_ids = response.context["following_ids"]

        self.assertIn(self.user1.id, following_ids)
        self.assertNotIn(self.user2.id, following_ids)

class FollowUserViewTestCase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.user1 = User.objects.get(username="@janedoe")

        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse("follow_user", args = [self.user1.id])

    def test_follow_need_log_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)

        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )

    def test_follow_need_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_follow_add_user(self):
        response = self.client.post(self.url)
        self.assertIn(self.user1, self.user.following.all())

        self.assertEqual(response.url, reverse("user_profile", args=[self.user1.username]))

class UnfollowUserViewTestCase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.user1 = User.objects.get(username="@janedoe")

        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse("unfollow_user", args = [self.user1.id])

    def test_unfollow_need_log_in(self):
        self.client.logout()
        redirect_url = reverse_with_next('log_in', self.url)

        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )

    def test_infollow_need_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_unfollow_remove_user(self):
        response = self.client.post(self.url)
        self.assertNotIn(self.user1, self.user.following.all())

        self.assertEqual(response.url, reverse("user_profile", args=[self.user1.username]))

class GetFollowerSummaryTestCase(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.user1 = User.objects.get(username='@janedoe')
        self.user2 = User.objects.get(username='@picklepeters')

        self.client.login(username=self.user.username, password='Password123')
        self.url = reverse("user_search")

        self.user1.followers.add(self.user2)

    def test_no_followers_returns_empty_string(self):
        no_follower = User.objects.create(username="@loneranger")
        summary = get_follower_summary(no_follower, self.user)
        self.assertEqual(summary,"")

    def test_mutal_friends_first(self):
        self.user.following.add(self.user1)

        summary = get_follower_summary(self.user1, self.user)
        self.assertIn("@johndoe",summary)
        self.assertIn("@picklepeters", summary)

    def test_correct_remaining_count_displayed(self):
        extra1 = User.objects.create(username="@people",email="people@example.com")
        extra2 = User.objects.create(username="@haiyah",email="haiyah@example.com")
        extra3 = User.objects.create(username="@addoil",email="addoil@example.com")
        self.user1.followers.add(extra1, extra2, extra3)

        summary = get_follower_summary(self.user1, self.user)

        self.assertIn("others", summary)