from django.test import TestCase
from recipes.models import Comment, User
from django import forms
from recipes.forms import CommentForm

class CommentFormTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.client.login(username=self.user.username, password='Password123')
        
        self.form_input = {
                "comment" : "testing",
        }

    def test_form_has_necessary_fields(self):
        form = CommentForm()
        self.assertIn('comment', form.fields)
        self.assertTrue(isinstance(form.fields['comment'], forms.CharField))

    def test_valid_comment_form_is_valid(self):
        form = CommentForm(data=self.form_input)
        self.assertTrue(form.is_valid)

    def test_blank_form_is_invalid(self):
        self.form_input['comment'] = ''
        form = CommentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_overly_long_comment_form_is_invalid(self):
        self.form_input['comment'] = 'x'*600
        form = CommentForm(data=self.form_input)
        self.assertFalse(form.is_valid())

