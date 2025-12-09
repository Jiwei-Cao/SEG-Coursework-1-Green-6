from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import MethodStep
from recipes.forms import MethodStepForm

from django.db import transaction

class EditMethodStepViewTestCase(TestCase):
    '''Tests for the edit_method_step view '''

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        
        self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123")
        self.method_step1 = MethodStep.objects.create(step_number="1", method_text="testing")

        self.recipe1.method_steps.add(self.method_step1)

        self.url = reverse("edit_method_step", kwargs={'recipe_id': f"{self.recipe1.pk}", 'step_id' : f"{self.method_step1.pk}"})

        self.form_input = {
                'method_text' : "test1",
        }


    def test_edit_method_step_url(self):
        self.assertEqual(self.url, f"/create_recipe/{self.recipe1.pk}/add_method/{self.method_step1.pk}/edit_method_step")

    def test_get_edit_method_step(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_method_step.html')

        self.assertIn('form', response.context)
        self.assertTrue(isinstance(response.context['form'], MethodStepForm))

        self.assertIn('recipe', response.context)
        self.assertEqual(response.context['recipe'], self.recipe1)

        self.assertIn('method_step', response.context)
        self.assertEqual(response.context['method_step'], self.method_step1)

    def test_get_edit_method_step_with_invalid_pk(self):

        invalid_url = reverse("edit_method_step", kwargs={'recipe_id': self.recipe1.pk, 'step_id' : 8})
        response = self.client.get(invalid_url, follow=True)
        self.assertEqual(response.status_code, 404)
        

    def test_save_valid_changes_post(self):
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_step_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_step_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)

        expected_redirect_url = reverse("add_method", kwargs={'recipe_id': f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        
        method_step = MethodStep.objects.get(pk = self.method_step1.pk)
        self.assertEqual(self.form_input['method_text'], method_step.method_text)
    
    def test_post_with_invalid_method_step_pk(self):
        invalid_url = reverse("edit_method_step", kwargs={'recipe_id': f"{self.recipe1.pk}", 'step_id' : 8})
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        response = self.client.post(invalid_url, self.form_input, follow=True)

        after_method_step_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_step_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)

        self.assertEqual(response.status_code, 404)


    def test_save_method_with_blank_method_text_is_invalid(self):
        self.form_input['method_text'] = ""
        self.assert_changes_are_invalid()

    def test_save_changes_with_overly_long_method_text_is_invalid(self):
        self.form_input['method_text'] = "x" * 300
        self.assert_changes_are_invalid()

        
    def assert_changes_are_invalid(self):
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        with transaction.atomic():
            response = self.client.post(self.url, self.form_input, follow=True)

        after_method_step_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_step_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_method_step.html')

        self.assertIn('form', response.context)
        self.assertTrue(isinstance(response.context['form'], MethodStepForm))
        self.assertIn('method_step', response.context)
        self.assertEqual(response.context['method_step'].method_text, self.method_step1.method_text)
        self.assertIn('recipe', response.context)
        self.assertEqual(response.context['recipe'], self.recipe1)