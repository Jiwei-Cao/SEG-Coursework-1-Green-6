from django import forms
from django.forms.models import modelformset_factory
from recipes.models import RecipeIngredient

class RecipeIngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'unit', 'ingredient']

# extra=1 indicates that 1  empty row is always added to allow the user to input their ingredients
RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=1, can_delete=True)
