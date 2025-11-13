from django import forms

class SearchRecipesForm(forms.Form):

	search_field = forms.CharField(label="search_field", max_length="64")