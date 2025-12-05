from django.test import TestCase
from recipes.models import User, Tag
from django import forms
from recipes.forms import SearchRecipesForm

class SearchRecipesFormTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        self.tag1 = Tag.objects.create(name="test_tag", colour='')

        self.form_input = {
                "search_field" : "test_search",
                "tags" : self.tag1,
                "order_by" : ("-created_at", "Newest"),
                # "ingredients" : "test_ingredient",
        }

    def test_form_has_necessary_fields(self):
        form = SearchRecipesForm()
        self.assertIn('search_field', form.fields)
        self.assertIn('tags', form.fields)
        # self.assertIn('ingredients', form.fields)
        self.assertIn('order_by', form.fields)

        self.assertTrue(isinstance(form.fields['search_field'], forms.CharField))
        self.assertTrue(isinstance(form.fields['tags'], forms.ModelMultipleChoiceField))
        # self.assertTrue(isinstance(form.fields['ingredients'], forms.CharField))
        self.assertTrue(isinstance(form.fields['order_by'], forms.ChoiceField))

    def test_valid_search_form_is_valid(self):
        form = SearchRecipesForm(data=self.form_input)
        self.assertTrue(form.is_valid)

    def test_overly_long_search_field_is_invalid(self):
        self.form_input['search_field'] = 'x'*100
        form = SearchRecipesForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # def test_overly_long_ingredients_field_is_invalid(self):
    #     self.form_input['ingredients'] = 'x'*100
    #     form = SearchRecipesForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())


    def test_blank_search_field_is_valid(self):
        self.form_input['search_field'] = ''
        form = SearchRecipesForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_blank_tags_field_is_valid(self):
        self.form_input['tags'] = None
        form = SearchRecipesForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # def test_blank_ingredients_field_is_valid(self):
    #     self.form_input['ingredients'] = ''
    #     form = SearchRecipesForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    def test_blank_order_by_field_is_valid(self):
        self.form_input['order_by'] = ''
        form = SearchRecipesForm(data=self.form_input)
        self.assertFalse(form.is_valid())





