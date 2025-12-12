from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe

class AllRecipesPageViewTest(TestCase):
    """Test of all recipes view"""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.url = reverse('all_recipes')
        self.user = User.objects.get(username='@johndoe')
        self.recipe1 = Recipe.objects.create(
            title="Chocolate Cake",
            description="Delicious chocolate dessert",
            # ingredients="Chocolate, Flour",
            img = "image/chocolate-cake.jpeg",
            # method="Bake",
            user=self.user
        )
        self.recipe2 = Recipe.objects.create(
            title="Apple Pie",
            description="Classic apple pie",
            img = "image/apple-pie.jpeg",
            # ingredients="Apple, Flour",
            # method="Bake",
            user=self.user
        )

    
    def test_all_recipes_page_url(self):
        self.assertEqual(self.url, '/all_recipes/')

    def test_get_all_recipes_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_recipes.html')
        self.assertIn(self.recipe1, response.context['recipe_list'])
        self.assertIn(self.recipe2, response.context['recipe_list'])

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_recipes_exists_in_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        recipes = response.context.get('recipe_list')
        self.assertIsNotNone(recipes)
        self.assertTrue(len(recipes) >= 0)
    
    def test_get_specific_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        url = reverse('get_recipe',args=[self.recipe1.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert self.recipe1.title.encode() in response.content

    def test_get_specific_recipe_not_found(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('get_recipe',args=[9999])
        response = self.client.get(url)
        assert response.status_code == 404

    def test_pagination_first_page(self):
        self.client.login(username=self.user.username, password='Password123')
        Recipe.objects.all().delete()
        for i in range(0,15):
            Recipe.objects.create(user=self.user, title=f"r{i}")

        response = self.client.get(self.url+"?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"].object_list),12)

    def test_pagination_second_page(self):
        self.client.login(username=self.user.username, password='Password123')
        Recipe.objects.all().delete()
        for i in range(0,15):
            Recipe.objects.create(user=self.user, title=f"r{i}")

        response = self.client.get(self.url+"?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page_obj"].object_list),3)

    def test_user_sees_public_and_own_and_followed_recipes(self):
        self.client.login(username=self.user.username, password='Password123')

        user2 = User.objects.get(username="@janedoe")
        user2.followers.add(self.user)

        public_recipes = Recipe.objects.create(user=user2, title="Public", public = True)
        followed_recipes = Recipe.objects.create(user=user2, title="Followed", public=False)
        own_recipes = Recipe.objects.create(user=self.user, title="Own", public=False)

        response = self.client.get(self.url)
        recipe_list = response.context["recipe_list"]

        self.assertIn(public_recipes, recipe_list)
        self.assertIn(followed_recipes, recipe_list)
        self.assertIn(own_recipes, recipe_list)
