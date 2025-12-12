from django.test import TestCase

from django.urls import reverse
from recipes.tests.helpers import reverse_with_next

from recipes.models import Recipe
from recipes.models import User
from recipes.models import MethodStep

class DeleteMethodStepViewTestCase(TestCase):
    '''Tests for the delete_method_step view '''

    fixtures = ['recipes/tests/fixtures/default_user.json','recipes/tests/fixtures/other_users.json',]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.recipe1 =  Recipe.objects.create(user=self.user, title="123", description="123")
        self.method_step1 =  MethodStep.objects.create(step_number=1, method_text="test_method")
        self.recipe1.method_steps.add(self.method_step1)
        self.url = reverse("delete_method_step", kwargs={'recipe_id': self.recipe1.pk, 'step_id': self.method_step1.pk})

    def test_delete_method_step_url(self):
        self.assertEqual(self.url, f"/create_recipe/{self.recipe1.pk}/add_method/{self.method_step1.pk}/delete_method_step")

    def test_get_delete_method_step_when_logged_out_redirects_user(self):
        self.client.logout()
        response = self.client.post(self.url, follow=True)
        expected_redirect_url  = reverse_with_next('log_in',self.url)
        self.assertRedirects(response, expected_redirect_url , status_code=302, target_status_code=200)

    def test_get_delete_method_step(self):
        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
    
    def test_delete_valid_method_step_post(self):
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        response = self.client.post(self.url, follow=True)
        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count-1)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count-1)
        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
        try:
            delete_method_step = MethodStep.objects.get(pk=self.method_step1.pk)
            deleted_recipe_method_step = self.recipe1.method_steps.get(pk=self.method_step1.pk)
        except MethodStep.DoesNotExist:
            pass
        else:
            self.fail("Method Step should've been removed after deletion")
    
    def test_delete_non_existent_method_step_post(self):
        invalid_url = reverse("delete_method_step", kwargs={'recipe_id': self.recipe1.pk, 'step_id':18})
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        response = self.client.post(invalid_url, follow=True)
        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)
        self.assertEqual(response.status_code, 404)

    def test_step_numbers_automatically_cascase_after_deletion(self):
        method_step2 = MethodStep.objects.create(step_number=2, method_text="test method 2")
        method_step3 = MethodStep.objects.create(step_number=3, method_text="test method 3")
        self.recipe1.method_steps.add(method_step2)
        self.recipe1.method_steps.add(method_step3)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(self.recipe1.method_steps.get(step_number=1), method_step2)
        self.assertEqual(self.recipe1.method_steps.get(step_number=2), method_step3)
        expected_redirect_url = reverse("add_method",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

    def test_delete_method_step_by_another_user_is_invalid(self):
        self.client.logout()
        self.user = User.objects.get(username='@janedoe')
        self.client.login(username=self.user.username, password='Password123')
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 403)
        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)
        
    def test_delete_method_step_outside_of_recipe_method_is_invalid(self):
        method_step2 = MethodStep.objects.create(step_number=2, method_text="test method 2")
        recipe2 = Recipe.objects.create(user=self.user, title="456", description="456")
        recipe2.method_steps.add(method_step2)
        invalid_url = reverse("delete_method_step", kwargs={'recipe_id': self.recipe1.pk, 'step_id':method_step2.pk})
        before_method_step_objects_count = MethodStep.objects.count()
        before_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        response = self.client.post(invalid_url, follow=True)
        after_method_steps_objects_count = MethodStep.objects.count()
        after_recipe_method_steps_count = self.recipe1.method_steps.all().count()
        self.assertEqual(after_method_steps_objects_count, before_method_step_objects_count)
        self.assertEqual(after_recipe_method_steps_count, before_recipe_method_steps_count)
        self.assertEqual(response.status_code, 404)


