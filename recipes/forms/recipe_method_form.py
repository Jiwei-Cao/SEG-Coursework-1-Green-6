from django import forms
from recipes.models import RecipeMethod

class RecipeMethodForm(forms.ModelForm):

    class Meta:
        model = RecipeMethod
        fields = ['recipe', 'step', 'order']