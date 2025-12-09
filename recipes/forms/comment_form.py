from django import forms
from recipes.models import Comment

class CommentForm(forms.Form):
    '''Form used to allow a user to create a comment'''
    comment = forms.CharField(
        label="Comment",
        widget=forms.Textarea(attrs={
            "placeholder": "Write your comment...",
            "rows": 2
        }),
        required=True,
        max_length=500,
    )
