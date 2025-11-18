from django import forms
from recipes.models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe 
        fields = ['title', 'description', 'ingredients', 'method', 'image']