"""Unit tests of the ingredient form."""
from django.test import TestCase
from recipes.forms.ingredient_form import IngredientForm
from django import forms
from recipes.models import Ingredient, User

class IngredientFormTestCase(TestCase):

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_ingredients.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'user': self.user,
            'name': 'Paprika',
            'category': 'SP'
        }
    
    def test_form_has_necessary_fields(self):
        form = IngredientForm()
        self.assertIn('name', form.fields)
        self.assertIn('category', form.fields)

        self.assertTrue(isinstance(form.fields['name'], forms.CharField))
        self.assertTrue(isinstance(form.fields['category'], forms.TypedChoiceField)) #

    def test_valid_ingredient_form(self):
            form = IngredientForm(data=self.form_input)
            self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['name'] = ''
        form = IngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid()) 

    def test_form_must_save_correctly(self):
        ingredient = Ingredient.objects.get(pk=1)

        form = IngredientForm(instance=ingredient, data=self.form_input)
        before_count = Ingredient.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        after_count = Ingredient.objects.count()

        self.assertEqual(after_count, before_count)

        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, 'Paprika')
        self.assertEqual(ingredient.category, 'SP')