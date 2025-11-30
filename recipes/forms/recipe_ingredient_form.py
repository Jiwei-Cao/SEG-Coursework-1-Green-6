from django import forms
from django.forms.models import modelformset_factory
from recipes.models import RecipeIngredient

class RecipeIngredientForm(forms.ModelForm):

    # These tweaks are needed to
    # prevent the user from changing the recipe of which they are editing ingredient
    # allow the form to be submitted to the backend for processing
    # the recipe is then explicitly set again the ingredients
    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.fields['recipe'].disabled = True
        self.fields['recipe'].required = False

    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'quantity', 'unit', 'ingredient']

RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0, can_delete=True)
