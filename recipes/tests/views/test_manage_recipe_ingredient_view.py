from django.forms.formsets import ManagementForm
from django.test import TestCase
from django.urls import reverse

from recipes.models import Recipe, User, RecipeIngredient, Unit, Ingredient
from recipes.forms import RecipeIngredientFormSet

class ManageRecipeIngredientFormTestCase(TestCase):

    fixtures=['recipes/tests/fixtures/default_user.json',
              'recipes/tests/fixtures/default_units.json',
              'recipes/tests/fixtures/default_recipe.json',
              'recipes/tests/fixtures/default_ingredients.json',
              ]
    
    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.recipe = Recipe.objects.get(pk=1)
        self.unit1 = Unit.objects.get(pk=1)
        self.ingredient1 = Ingredient.objects.get(pk=1)
        self.recipe_ingredient1 = RecipeIngredient.objects.create(user=self.user, recipe=self.recipe, quantity=4, unit=self.unit1, ingredient=self.ingredient1)

        self.url = reverse("manage_recipe_ingredient", kwargs={'recipe_id': f"{self.recipe.id}"})
        
    def test_manage_recipe_ingredient_url(self):
        self.assertEqual(self.url, f"/manage_recipe_ingredient/{self.recipe.pk}/")

    def test_get_manage_recipe_ingredient(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe_ingredient.html')
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertTrue(isinstance(form, ManagementForm))
        self.assertFalse(form.is_bound)

    def test_page_renders_with_existing_data(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.recipe_ingredient1.ingredient)
        self.assertContains(response, self.recipe_ingredient1.quantity)
        self.assertContains(response, self.recipe_ingredient1.unit)
        self.assertTemplateUsed('create_recipe_ingredient.html')

    def test_valid_formset_post(self):
        before_count = RecipeIngredient.objects.count()
        forms = []
        for recipe_ingredient in RecipeIngredient.objects.all():
            form = {
                "id": recipe_ingredient.pk,
                "quantity": str(recipe_ingredient.quantity),
                "unit": recipe_ingredient.unit.id,
                "ingredient": recipe_ingredient.ingredient.id,
            }
            forms.append(form)
        additional_form = {"id": "", "ingredient": 3, "quantity": 0.10, "unit": 1}
        forms.append(additional_form)
        payload = self.build_formset_data(forms=forms)
        response = self.client.post(self.url, payload, follow=True)
        after_count = RecipeIngredient.objects.count()
        self.assertEqual(after_count, before_count +1)
        expected_url = reverse('manage_recipe_ingredient', args=[self.recipe.id])
        self.assertRedirects(response, expected_url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def test_delete_recipe_ingredient(self):
        before_count = RecipeIngredient.objects.count()
        forms = []
        for recipe_ingredient in RecipeIngredient.objects.all():
            form = {
                "id": recipe_ingredient.pk,
                "quantity": str(recipe_ingredient.quantity),
                "unit": recipe_ingredient.unit.id,
                "ingredient": recipe_ingredient.ingredient.id,
            }
            forms.append(form)
        del forms[0]    
        delete_url = reverse("manage_recipe_ingredient", args=[self.recipe.id])
        response = self.client.post(delete_url, forms, follow=True)
        after_count = RecipeIngredient.objects.count()
        self.assertEqual(after_count, before_count-1)
        expected_url = reverse('manage_recipe_ingredient', args=[self.recipe.id])
        self.assertRedirects(response, expected_url)
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)

    def build_formset_form_data(self, form_number, **data):
        form = {}
        for key, value in data.items():
            form_key = f"recipe_ingredient-{form_number}-{key}"
            form[form_key] = value
        return form

    def build_formset_data(self, forms, **common_data):
        formset_dict = {
            "recipe_ingredient-TOTAL_FORMS": f"{len(forms)}",
            "recipe_ingredient-MAX_NUM_FORMS": "1000",
            "recipe_ingredient-MIN_NUM_FORMS": "0",
            "recipe_ingredient-INITIAL_FORMS": "3"
        }
        formset_dict.update(common_data)
        for i, form_data in enumerate(forms):
            form_dict = self.build_formset_form_data(form_number=i, **form_data)
            formset_dict.update(form_dict)
        return formset_dict