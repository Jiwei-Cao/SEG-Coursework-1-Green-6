from django.test import TestCase
from recipes.models import MethodStep, User
from django import forms
from recipes.forms import MethodStepForm

class MethodStepFormTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        
        self.form_input = {
                "step_number" : 1,
                "method_text" : "testing",
        }

    def test_form_has_necessary_fields(self):
        form = MethodStepForm()
        self.assertIn('step_number', form.fields)
        self.assertIn('method_text', form.fields)

        self.assertTrue(isinstance(form.fields['step_number'], forms.IntegerField))
        self.assertTrue(isinstance(form.fields['method_text'], forms.CharField))

    
    def test_valid_method_step_form_is_valid(self):
        form = MethodStepForm(data=self.form_input)
        self.assertTrue(form.is_valid())
 
    def test_blank_step_number_is_invalid(self):
        self.form_input['step_number'] = ''
        form = MethodStepForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_method_text_is_invalid(self):
        self.form_input['method_text'] = ''
        form = MethodStepForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_overly_high_step_number_is_invalid(self):
        self.form_input['step_number'] = 23
        form = MethodStepForm(data=self.form_input)
        self.assertFalse(form.is_valid())
 

    def test_overly_long_method_text_form_is_invalid(self):
        self.form_input['method_text'] = 'x' * 300
        form = MethodStepForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_form_saves_correctly(self):
        form = MethodStepForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before_count = MethodStep.objects.count()

        form.save()

        after_count = MethodStep.objects.count()
        self.assertEqual(after_count, before_count + 1)

        method_step = MethodStep.objects.get(pk=1)
        self.assertEqual(method_step.step_number, 1)
        self.assertEqual(method_step.method_text, "testing" )



