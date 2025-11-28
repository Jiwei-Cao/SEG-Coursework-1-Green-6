from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import MethodStep

import datetime

class AddMethodViewTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        
        self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123")
        self.url = reverse("add_method", kwargs={'recipe_id': f"{self.recipe1.pk}"})

        self.form_input = {
                'step_number' : 1,
                'method_text' : "testing"
        }

    def test_add_method_url(self):
        self.assertEqual(self.url, f"/create_recipe/{self.recipe1.pk}/add_method/")

    def test_get_add_method_(self):
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_method.html')


    def test_create_valid_method_step_post(self):
        before_method_steps_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.form_input['operation'] = 'add_step'
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
        self.form_input['operation'] = 'add_step'
        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_steps_objects_count, before_method_steps_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)
        
        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)


    def test_delete_valid_method_step_post(self):
        method_step = MethodStep(step_number=self.form_input['step_number'], method_text=self.form_input['method_text'])
        method_step.save()
        self.recipe1.method_steps.add(method_step)

        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(before_method_step_objects_count, 1)
        self.assertEqual(before_recipe_method_steps_count, 1)

        self.form_input['step_clicked'] = method_step.pk
        self.form_input['operation'] = 'delete_step'
        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count-1)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count-1)

        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

        try:
            delete_method_step = MethodStep.objects.get(pk=method_step.pk)
        except MethodStep.DoesNotExist:
            pass
        else:
            self.fail("Method Step should've been removed after deletion")

        try:
            deleted_recipe_method_step = self.recipe1.method_steps.get(pk=method_step.pk)
        except MethodStep.DoesNotExist:
            pass
        else:
            self.fail("Method Step should've been removed after deletion")



    def test_delete_non_existent_method_step_post(self):
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(before_method_step_objects_count, 0)
        self.assertEqual(before_recipe_method_steps_count, 0)

        self.form_input['operation'] = 'delete_step'
        response = self.client.post(self.url, self.form_input, follow=True)

        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()

        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)

        self.assertEqual(response.status_code, 404)



 
    


    '''
    def test_add_method_step_with_duplicate_step_numbers_is_invalid(self):
    
    def test_add_method_step_with_0_step_number_is_invalid(self):
        
    def test_add_method_step_with_0_step_number_is_invalid(self):
    
    def test_add_too_many_method_steps(self):
    '''