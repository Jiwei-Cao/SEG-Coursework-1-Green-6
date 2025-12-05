from django.test import TestCase
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe, User, Ingredient, Tag, RecipeIngredient, Unit

from recipes.models import Recipe
from recipes.models import User, Ingredient, Unit, RecipeIngredient


class BrowseRecipesTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		self.url = reverse("all_recipes")

		self.tag1 = Tag.objects.create(name="test_tag", colour='')
		self.ingredient = Ingredient.objects.create(user=self.user, name="test_ingr", category="None")
		self.unit = Unit.objects.create(user=self.user, name="grams", symbol="g")


		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123" )
		self.recipe1.tags.add(self.tag1)

		self.recipe2 =  Recipe.objects.create(user=self.user, title="456",description="abc")
		self.recipe_ingredient = RecipeIngredient.objects.create(user=self.user, recipe=self.recipe2, quantity="1", unit=self.unit, ingredient=self.ingredient)

		self.recipe_list = [self.recipe1, self.recipe2]

		self.form_input = {
							'search_field' : "",
							'tags': [],
							'order_by': '',# ("-created_at", "Newest"), 
							'ingredients': [], #self.ingredient
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
		self.form_input['search_field'] = "testing"

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


	def test_get_all_recipes_with_tag_search(self):

		self.form_input['tags'] = [self.tag1]

		tag_ids = ','.join(str(tag.id) for tag in self.form_input['tags'])
		search_query_string = f'?tags={tag_ids}'
		self.url = reverse("all_recipes")  + search_query_string
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'all_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		filtered_recipes = Recipe.objects.filter(tags__id__in=tag_ids).distinct().count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), filtered_recipes) 


	def test_get_all_recipes_with_ingredient_search(self):
		self.form_input['ingredients'] = [self.ingredient]

		ingredient_ids = ','.join(str(tag.id) for tag in self.form_input['ingredients'])
		search_query_string = f'?ingredients={ingredient_ids}'
		self.url = reverse("all_recipes")  + search_query_string
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'all_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		filtered_recipes = Recipe.objects.filter(id__in=RecipeIngredient.objects.filter(ingredient__id__in=ingredient_ids)).distinct().count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), filtered_recipes) 

	def test_get_all_recipes_with_order_by_date_created(self):
		self.form_input['order_by'] = "created_at"
		self._test_get_order_by()

		self.form_input['order_by'] = "-created_at"
		self._test_get_order_by()

	def test_get_all_recipes_with_order_by_favourites(self):
		self.form_input['order_by'] = "favourites"
		self._test_get_order_by()

		self.form_input['order_by'] = "-favourites"
		self._test_get_order_by()

	def test_get_all_recipes_with_order_by_ratings(self):
		self.form_input['order_by'] = "rating"
		self._test_get_order_by()

		self.form_input['order_by'] = "-rating"
		self._test_get_order_by()

	def _test_get_order_by(self):
		search_query_string = f'?order_by={self.form_input['order_by']}'
		self.url = reverse("all_recipes")  + search_query_string
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'all_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), Recipe.objects.count())


	#def test_all_recipes_with_all_searches(self):


		

	def test_post_with_valid_data(self):

		self.form_input['search_field'] = "testing"
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