from django.test import TestCase
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe, User, Ingredient, Tag, RecipeIngredient, Unit

from recipes.models import Recipe
from recipes.models import User, Ingredient, Unit, RecipeIngredient, Tag

from recipes.views import build_query_params


class BrowseRecipesTestCase(TestCase):

	fixtures = [
		'recipes/tests/fixtures/default_user.json', 
		'recipes/tests/fixtures/other_users.json',
		'recipes/tests/fixtures/default_ingredients.json'
		]

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

		expected_recipe_list = Recipe.objects.all()
		tag_ids = [tag.id for tag in self.form_input['tags']]
		for tag_id in tag_ids:
			expected_recipe_list = expected_recipe_list.filter(tags__id=tag_id)
		self.assertIn('recipe_list', response.context)
		self.assertQuerySetEqual((response.context['recipe_list']), expected_recipe_list)


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

	def test_post_with_valid_data(self):
		self.form_input['search_field'] = "testing"
		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		expected_redirect_url = reverse("all_recipes") + search_query_string

		response = self.client.post(self.url, self.form_input)
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		response = self.client.get(expected_redirect_url)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertIsInstance(form, SearchRecipesForm)
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

	def test_query_param_with_only_tags(self):
		tags = Tag.objects.filter(pk__in=[1,2])
		result = build_query_params(
			search_val = None,
			tags = list(tags),
			order_by = None,
			ingredients=None
		)

		self.assertEqual(result, "?tags=1,2")
	
	def test_params_with_order_by(self):
		result = build_query_params(
			search_val=None,
			tags=None,
			order_by='created_at',
			ingredients=None
		)

		self.assertEqual(result, "?order_by=created_at")

	def test_params_with_ingredients(self):
		ingredients = Ingredient.objects.filter(pk__in=[1,3])
		result = build_query_params(
			search_val=None,
			order_by=None,
			tags=None,
			ingredients= ingredients
		)

		self.assertEqual(result, "?ingredients=1,3")

	def test_params_tags_and_order_by(self):
		tags = Tag.objects.filter(pk__in=[3])
		result = build_query_params(
			search_val = None,
			tags = list(tags),
			order_by="-rating",
			ingredients=None
		)
		self.assertEqual(result,"?tags=3&order_by=-rating")

	def test_params_ingredients_and_order_by(self):
		ingredients = Ingredient.objects.filter(pk__in=[1])
		result = build_query_params(
			search_val = None,
			tags = None,
			order_by="favourites",
			ingredients=ingredients
		)
		self.assertEqual(result, "?order_by=favourites&ingredients=1")

	def test_all_params(self):
		tags = Tag.objects.filter(pk__in=[5])
		ingredients=Ingredient.objects.filter(pk__in=[1,2])
		result=build_query_params(
			search_val="cake",
			tags=list(tags),
			order_by="-favourites",
			ingredients=ingredients
		)
		self.assertEqual(result,"?search_val=cake&tags=5&order_by=-favourites&ingredients=1,2")

	def test_empty_params(self):
		result=build_query_params(None,None,None,None)
		self.assertEqual(result,"")