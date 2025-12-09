from django.test import TestCase
from django.urls import reverse
from recipes.tests.helpers import reverse_with_next
from recipes.models import User, UserIngredient, Unit
from recipes.forms import UserIngredientForm

class DeleteIngredientViewTestCase(TestCase):

    fixtures=['recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/default_units.json',
            'recipes/tests/fixtures/default_user_ingredients.json',
            'recipes/tests/fixtures/default_ingredients.json',
            'recipes/tests/fixtures/default_tags.json'
              ]
    
    def setUp(self):
        self.url = reverse('cupboard')
        self.unit = Unit.objects.get(name = 'tablespoon')
        self.user_ingredient= UserIngredient.objects.get(name='Tomato')
        self.form_input = {
            'name' : 'new ingredient',
            'category' : UserIngredient.BUTCHERY,
            'quantity' : 3,
            'unit' : Unit.objects.get(name='tablespoon').pk
        }

        self.url = reverse('delete_ingredient', args=[self.user_ingredient.id])
        self.client.login(username="@johndoe", password="Password123")
    
    def test_delete_ingredient_url(self):
        self.assertEqual(self.url, f"/cupboard/{self.user_ingredient.id}/delete")

    def test_get_delete_ingredient_request_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_delete_ingredient_redirects_if_not_logged_in(self):
        self.client.logout()
        response = self.client.post(self.url)
        expected_url = reverse_with_next('log_in',self.url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
    
    def test_delete_ingredient_with_invalid_id(self):
        url = reverse('delete_ingredient', args=[self.user_ingredient.id + 1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
    
    def test_valid_delete_ingredient_request(self):
        ingredient_id = self.user_ingredient.id
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

        self.assertFalse(UserIngredient.objects.filter(id=ingredient_id).exists())
    
    def test_delete_ingredient_redirects_to_cupboard(self):
        response = self.client.post(self.url, follow=True)
        self.assertRedirects(response, reverse('cupboard'))

    def test_unauthorised_user_delete_request_rejects(self):
        self.client.logout()

        user2 = User.objects.create(username="@Janedoe", email="janedoe@example.com")
        user2.set_password("Password123")
        user2.save()

        self.client.login(username="@Janedoe", password="Password123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)


        #         self.ingredient_data = {
        #     "user": self.user,
        #     "name": "Hemlock",
        #     "category": UserIngredient.SPICE,
        #     "quantity": 7,
        #     'unit' : Unit.objects.get(name='tablespoon').pk
        # }
        # self.ingredient = UserIngredient.objects.create(
        #     user = self.ingredient_data['user'],
        #     name = self.ingredient_data['name'],
        #     category = self.ingredient_data['category'],
        #     quantity = self.ingredient_data['quantity'],
        #     unit = self.ingredient_data['unit']
        # )