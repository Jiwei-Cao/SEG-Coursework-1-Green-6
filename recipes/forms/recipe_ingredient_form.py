from django import forms
from django.forms.models import modelformset_factory
from recipes.models import RecipeIngredient

class RecipeIngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['quantity', 'unit', 'ingredient']

RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=10, can_delete=True)
