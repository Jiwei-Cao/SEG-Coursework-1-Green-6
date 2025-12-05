"""Unit tests of the recipe_ingredient form."""
from django.test import TestCase
from recipes.forms.recipe_ingredient_form import RecipeIngredientForm
from django import forms
from recipes.models import RecipeIngredient, Ingredient, User, Unit, Recipe

class RecipeIngredientFormTestCase(TestCase):

    fixtures = [
        'recipes/tests/fixtures/default_user.json', 
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_recipe.json',
        'recipes/tests/fixtures/default_ingredients.json',
        'recipes/tests/fixtures/default_units.json',
        'recipes/tests/fixtures/default_recipe_ingredients.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.get(title="Tomato Soup")
        self.unit = Unit.objects.get(name='tablespoon')
        self.ingredient = Ingredient.objects.get(name="Paprika")
        self.form_input = {
            'user': self.user,
            'recipe': self.recipe,
            'quantity': 5,
            'unit': self.unit,
            'ingredient': self.ingredient
        }
    
    def test_form_has_necessary_fields(self):
        form = RecipeIngredientForm()
        #self.assertIn('user', form.fields)
        #self.assertIn('recipe', form.fields)
        self.assertIn('quantity', form.fields)
        #self.assertIn('unit', form.fields)
        #self.assertIn('ingredient', form.fields)

        #self.assertTrue(isinstance(form.fields['user'], forms.CharField))
        self.assertTrue(isinstance(form.fields['quantity'], forms.DecimalField))
        #self.assertTrue(isinstance(form.fields['unit'], forms.CharField))

    def test_valid_ingredient_form(self):
            form = RecipeIngredientForm(data=self.form_input)
            self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['quantity'] = ''
        form = RecipeIngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid()) 

    def test_form_must_save_correctly(self):
        recipe_ingredient = RecipeIngredient.objects.get(pk=1)

        form = RecipeIngredientForm(instance=recipe_ingredient, data=self.form_input)
        before_count = RecipeIngredient.objects.count()
        self.assertTrue(form.is_valid())
        form.save()
        after_count = RecipeIngredient.objects.count()

        self.assertEqual(after_count, before_count)

        recipe_ingredient.refresh_from_db()
        self.assertEqual(recipe_ingredient.quantity, 5)
        self.assertEqual(recipe_ingredient.unit, Unit.objects.get(name='tablespoon'))