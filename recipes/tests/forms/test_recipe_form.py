"""Unit tests of the recipe form."""
from django.test import TestCase
from recipes.forms.recipe_form import RecipeForm
from django import forms
from recipes.models import Recipe

class RecipeFormTestCase(TestCase):
    """Unit tests of the recipe form."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/default_recipe.json'
    ]

    def setUp(self):
        self.form_input = {
            'title': 'Pasta Bolognese',
            'description': 'A simple pasta recipe',
            'ingredients': 'Pasta\nTomato sauce\nBeef mince',
            'method': 'Boil pasta.\nCook beef.\nMix with sauce.'
        }
    
    def test_form_has_necessary_fields(self):
        form = RecipeForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('method', form.fields)

        self.assertTrue(isinstance(form.fields['title'], forms.CharField))
        self.assertTrue(isinstance(form.fields['description'], forms.CharField))
        self.assertTrue(isinstance(form.fields['ingredients'], forms.CharField))
        self.assertTrue(isinstance(form.fields['method'], forms.CharField))

    
    

    def test_form_must_save_correctly(self):
        recipe = Recipe.objects.get(pk=1)

        form = RecipeForm(instance=recipe, data=self.form_input)
        before_count = Recipe.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        after_count = Recipe.objects.count()

        self.assertEqual(after_count, before_count)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, 'Pasta Bolognese')
        self.assertEqual(recipe.description, 'A simple pasta recipe')
        self.assertEqual(
            recipe.ingredients,
            'Pasta\nTomato sauce\nBeef mince'
        )
        self.assertEqual(
            recipe.method,
            'Boil pasta.\nCook beef.\nMix with sauce.'
        )