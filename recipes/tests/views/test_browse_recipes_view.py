from django.test import TestCase
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe
from recipes.models import User, Ingredient, Unit, RecipeIngredient


class BrowseRecipesTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		self.url = reverse("all_recipes")

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

		self.recipe_list = [self.recipe1, self.recipe2]


		self.form_input = {
							'search_field' : "12",
							'tags':[],
							'order_by':''
						   }

	def test_all_recipes_url(self):
		self.assertEqual(self.url, "/all_recipes/")


	def test_get_all_recipes_without_search_value(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'all_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_get_all_recipes_with_search_value(self):
		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		self.url = reverse("all_recipes")  + search_query_string
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'all_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		filtered_recipes = Recipe.objects.filter(title__contains=search_val).count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), filtered_recipes) 
		
		

	def test_post_with_valid_data(self):
		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		expected_redirect_url = reverse("all_recipes") + search_query_string

		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		filtered_recipes = Recipe.objects.filter(title__contains=search_val).count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), filtered_recipes) 


	def test_post_with_invalid_data(self):
		self.form_input['search_field'] = ''

		expected_redirect_url = reverse("all_recipes")

		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_overly_long_search_is_invalid(self):
		self.form_input['search_field'] = "x" * 256

		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertEqual(response.status_code, 200)

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)