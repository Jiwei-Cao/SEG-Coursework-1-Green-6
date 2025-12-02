from django import forms
from recipes.models import Comment

class CommentForm(forms.Form):
    comment = forms.CharField(
        label="Comment",
        widget=forms.Textarea(attrs={
            "placeholder": "Write your comment...",
            "rows": 2
        }),
        required=True,
        max_length=500,
    )
    #comment = forms.CharField(label="Comment", required=True)