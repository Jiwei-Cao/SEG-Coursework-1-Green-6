from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import MethodStep

from recipes.forms import MethodStepForm

from django.db.utils import IntegrityError
from django.db import transaction

class AddMethodViewTestCase(TestCase):
    '''Tests for the add_method view '''

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        
        self.recipe1 =  Recipe.objects.create(user=self.user, title="123", description="123")
        self.url = reverse("add_method", kwargs={'recipe_id': f"{self.recipe1.pk}"})

        self.form_input = {
                'method_text' : "testing"
        }

    def test_add_method_url(self):
        self.assertEqual(self.url, f"/create_recipe/{self.recipe1.pk}/add_method/")

    def test_get_add_method(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_method.html')

        self.assertIn('form', response.context)
        self.assertTrue(isinstance(response.context['form'], MethodStepForm))
        self.assertFalse(response.context['form'].is_bound)

        self.assertIn('recipe', response.context)
        self.assertEqual(response.context['recipe'], self.recipe1)

    def test_get_add_method_step_with_invalid_recipe_pk(self):
        invalid_url = reverse("add_method", kwargs={'recipe_id': 8})
        response = self.client.get(invalid_url, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_create_valid_method_step_post(self):
        before_method_steps_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_steps_objects_count, before_method_steps_objects_count + 1)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count + 1)

        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_create_invalid_method_step_post(self):
        before_method_steps_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.form_input['method_text'] = ''
        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_steps_objects_count, before_method_steps_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)
        
        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)



