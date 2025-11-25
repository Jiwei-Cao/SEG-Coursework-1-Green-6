from django import forms
from recipes.models import Recipe, Tag
from django_select2.forms import ModelSelect2MultipleWidget

class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=ModelSelect2MultipleWidget(
            model=Tag,
            search_fields=['name__icontains'],
            attrs={
                'data-placeholder': 'Search tags',
                'style':'width: 20%',
                'data-minimum-input-length':0
            }
        ))
    class Meta:
        model = Recipe 
        fields = ['title', 'description', 'img','tags']