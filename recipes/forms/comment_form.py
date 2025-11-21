from django import forms
from recipes.models import Comment

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", required=True)