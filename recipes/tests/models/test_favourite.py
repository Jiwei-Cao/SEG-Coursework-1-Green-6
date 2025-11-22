from django.test import TestCase
from django.urls import reverse
from recipes.models import Favourite, User, Recipe

class FavouriteModelTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):

		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123",ingredients="123",method="123")

		self.favourite = Favourite.objects.create(user=self.user, recipe=self.recipe1)


	def test_valid_favourite(self):
		try:
			self.favourite.full_clean()
		except ValidationError:
			self.fail("Favourite object should be valid")


	def test_user_cannot_favourite_recipe_more_than_once(self):
		try:
			with transaction.atomic():
				with self.assertRaises(IntegrityError):
					favourite2 = Favourite.objects.create(user=self.user, recipe=self.recipe1)
		except:
			pass
		else: 
			self.fail("Shouldn't be able to have 2 duplicate favourite records")