from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe

class AllRecipesPageViewTest(TestCase):
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
            ingredients="Chocolate, Flour",
            image = "recipe_image/chocolate-cake.jpeg",
            method="Bake",
            user=self.user
        )
        self.recipe2 = Recipe.objects.create(
            title="Apple Pie",
            description="Classic apple pie",
            image = "recipe_image/apple-pie.jpeg",
            ingredients="Apple, Flour",
            method="Bake",
            user=self.user
        )

    
    def test_all_recipes_page_url(self):
        self.assertEqual(self.url, '/all_recipes/')

    def test_get_all_recipes_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_recipes.html')
        self.assertIn(self.recipe1, response.context['recipes'])
        self.assertIn(self.recipe2, response.context['recipes'])

        user = response.context['user']
        self.assertTrue(isinstance(user, User))
        self.assertEqual(self.user, user)

    def test_recipes_exists_in_page(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        recipes = response.context.get('recipes')
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
