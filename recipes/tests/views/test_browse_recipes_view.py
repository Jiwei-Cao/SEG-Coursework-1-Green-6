from django.test import TestCase

from django.urls import reverse
from django.db import transaction
from django.db.utils import IntegrityError


from recipes.forms import SearchRecipesForm
from recipes.forms import FavouriteForm


from recipes.models import Recipe
from recipes.models import User
from recipes.models import Favourite


class BrowseRecipesTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		self.url = reverse("browse_recipes")

		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123",ingredients="123",method="123")
		self.recipe2 =  Recipe.objects.create(user=self.user, title="456",description="abc",ingredients="456",method="abc")

		self.recipe_list = [self.recipe1, self.recipe2]


		self.form_input = {
							'search_field' : "12",
							'form_type': '',
							'favourite_recipe': '',
							'recipe_clicked': ''
						   }

	def test_browse_recipes_url(self):
		self.assertEqual(self.url, "/browse_recipes/")


	def test_get_browse_recipes_without_search_value(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'browse_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_get_browse_recipes_with_search_value(self):
		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		self.url = reverse("browse_recipes")  + search_query_string
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'browse_recipes.html')

		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertFalse(form.is_bound)

		filtered_recipes = Recipe.objects.filter(title__contains=search_val).count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual(len((response.context['recipe_list'])), filtered_recipes) 
		
		

	def test_post_with_valid_data(self):
		self.form_input['form_type'] = 'search_form'

		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		expected_redirect_url = reverse("browse_recipes") + search_query_string

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
		self.form_input['form_type'] = 'search_form'

		expected_redirect_url = reverse("browse_recipes")

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
		self.form_input['form_type'] = "search_form"

		expected_redirect_url = reverse("browse_recipes")

		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_post_data_to_favourite_form_without_search_value(self):
		self.form_input['search_field'] = ''
		self.form_input['form_type'] = 'favourite_form'

		expected_redirect_url = reverse("browse_recipes") 
		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_post_data_to_favourite_form_with_search_value(self):
		self.form_input['form_type'] = 'favourite_form'
		response = self.client.post(self.url, self.form_input, follow=True)

		search_val = self.form_input['search_field']
		search_query_string = f'?search_val={search_val}'
		expected_redirect_url = reverse("browse_recipes") + search_query_string

		expected_redirect_url = reverse("browse_recipes") 
		response = self.client.post(self.url, self.form_input, follow=True)
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		self.assertIn('form', response.context)
		form = response.context['form']
		self.assertTrue(isinstance(form, SearchRecipesForm))

		recipes_count = Recipe.objects.count()
		self.assertIn('recipe_list', response.context)
		self.assertEqual((response.context['recipe_list']).count(), recipes_count)


	def test_favourite_unfavourited_recipe(self):
		self.form_input['form_type'] = 'favourite_form'
		self.form_input['favourite_recipe'] = 'favourite_recipe'
		self.form_input['recipe_clicked'] = (self.recipe1).pk

		before_favourite_count = Favourite.objects.count()
		
		response = self.client.post(self.url, self.form_input, follow=True)

		after_favourite_count = Favourite.objects.count()
		self.assertEqual(after_favourite_count, before_favourite_count + 1)

		expected_redirect_url = reverse("browse_recipes") 
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		self.assertIn('user_favourite_objects', response.context)
		favourited_recipes = response.context['user_favourite_objects']
		

		self.assertEqual(len(favourited_recipes), after_favourite_count)


	def test_favourite_already_favourited_recipe(self):
		self.form_input['form_type'] = 'favourite_form'
		self.form_input['favourite_recipe'] = 'favourite_recipe'
		self.form_input['recipe_clicked'] = (self.recipe1).pk

		favourite_object = Favourite.objects.create(user=self.user, recipe=self.recipe1)
		before_favourite_count = Favourite.objects.count()
		try:
			with transaction.atomic():	
					response = self.client.post(self.url, self.form_input, follow=True)
		except:
			pass
		else:
			self.fail("Shouldn't be able to favourite an already favourited recipe")
		
		after_favourite_count = Favourite.objects.count()
		self.assertEqual(after_favourite_count, before_favourite_count)


	def test_unfavourite_favourited_recipe(self):

		#favourites the recipe first
		self.form_input['form_type'] = 'favourite_form'
		self.form_input['recipe_clicked'] = (self.recipe1).pk

		favourite_object = Favourite.objects.create(user=self.user, recipe=self.recipe1)
		favourite_id = favourite_object.pk


		self.form_input['favourite_recipe'] = 'unfavourite_recipe'
		before_favourite_count = Favourite.objects.count()
		response = self.client.post(self.url, self.form_input, follow=True)
		after_favourite_count = Favourite.objects.count()
		self.assertEqual(after_favourite_count, before_favourite_count - 1)

		expected_redirect_url = reverse("browse_recipes") 
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
		self.assertIn('user_favourite_objects', response.context)
		favourited_recipes = response.context['user_favourite_objects']
		
		self.assertEqual(len(favourited_recipes), after_favourite_count)

		try:
			favourite = Favourite.objects.get(pk=favourite_id)
		except Favourite.DoesNotExist:
			pass
		else: 
			self.fail("Favourite object should've been removed after unfavouriting")

	def test_unfavourite_already_unfavourited_recipe(self):

		self.form_input['form_type'] = 'favourite_form'
		self.form_input['favourite_recipe'] = 'unfavourite_recipe'
		self.form_input['recipe_clicked'] = (self.recipe1).pk
		
		before_favourite_count = Favourite.objects.count()
		try:
			with transaction.atomic():
				with self.assertRaises(IntegrityError):
					response = self.client.post(self.url, self.form_input, follow=True)
		except:
			pass
		else:
			self.fail("Shouldn't be able to unfavourite an already unfavourited recipe")
		
		after_favourite_count = Favourite.objects.count()
		self.assertEqual(after_favourite_count, before_favourite_count)



	#def test_generate_search_query_string(self):


	#def test_map_recipe_to_favourite_count(self):
