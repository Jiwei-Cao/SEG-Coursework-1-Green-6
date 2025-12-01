from django import forms
from recipes.models import Tag
from django_select2.forms import ModelSelect2MultipleWidget

class SearchRecipesForm(forms.Form):
    search_field = forms.CharField( 
        label="Search", 
        max_length="64",
        required=False, 
        widget=forms.TextInput(
            {'placeholder':'Enter your search here'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        required=False, 
        widget=ModelSelect2MultipleWidget( 
            model=Tag, 
            search_fields=['name__icontains'], 
            attrs={
                'data-placeholder': 'Search tags',
                'style':'width: 100%',
                'data-minimum-input-length':0}))
    ingredients = forms.CharField(
        label="Ingredients",
        max_length="64",
        required=False,
        widget=forms.TextInput(
            {'placeholder':"Search by ingredients"}))
    order_by = forms.ChoiceField(
    	choices=[
    		('-created_at', 'Newest'),
    		('created_at', 'Oldest'),
    		('-rating', 'Highest rated'),
    		('rating', 'Lowest rated'),
    		('favourites', 'Most favourited'),
    		('-favourites', 'Least favourited')
        ],
    	required=False
    )

