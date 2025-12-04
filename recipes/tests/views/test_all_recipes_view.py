from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, Ingredient, Unit, RecipeIngredient

class AllRecipesPageViewTest(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]
    def setUp(self):
        self.url = reverse('all_recipes')
        self.user = User.objects.get(username='@johndoe')
        self.recipe1 = Recipe.objects.create(title="Test Recipe", description="desc", user=self.user)
        self.ingredient1,_ = Ingredient.objects.get_or_create(name="Flour",user=self.user)
        self.unit,_ = Unit.objects.get_or_create(name="kgs",symbol="kgs",user=self.user)

        self.recipe_ingredient = RecipeIngredient.objects.create(
            user=self.user,
            recipe = self.recipe1,
            ingredient = self.ingredient1,
            unit = self.unit,
            quantity=2
        )

        self.recipe2 = Recipe.objects.create(title="Tomato souop", description="desc", user=self.user)
        self.ingredient2,_ = Ingredient.objects.get_or_create(name="Tomato",user=self.user)


        self.recipe_ingredient = RecipeIngredient.objects.create(
            user=self.user,
            recipe = self.recipe2,
            ingredient = self.ingredient2,
            unit = self.unit,
            quantity=1
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
