from django import forms
from recipes.models import UserIngredient

class UserIngredientForm(forms.ModelForm):

    class Meta:
        model = UserIngredient
        fields = ['name', 'category', 'quantity', 'unit']