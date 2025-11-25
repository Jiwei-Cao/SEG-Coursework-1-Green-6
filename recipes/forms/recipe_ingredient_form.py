from django import forms
from recipes.models import RecipeIngredient

class RecipeIngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'quantity', 'unit','ingredient']