from django.test import TestCase
from recipes.models import Comment, User
from django.core.exceptions import ValidationError


import datetime
from django.utils.timezone import make_aware

class CommentModelTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):

		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')

		self.comment_text = "abc"
		self.date_published = make_aware(datetime.datetime(2025, 1, 1))

		self.comment = Comment(user=self.user, comment=self.comment_text, date_published=self.date_published )
		self.comment.save()


	def test_valid_comment(self):
		self._assert_comment_is_valid()
		
	def test_comment_cannot_be_blank(self):
		self.comment.comment = ''
		with self.assertRaises(ValidationError):
			self.comment.full_clean()		
		
	def test_comment_cannot_be_over_500_characters_long(self):
		self.comment.comment = ('x' * 600)
		self._assert_comment_is_invalid()	
	
	def test_comment_with_non_date_date_published_field_is_invalid(self):
		self.comment.date_published = "not a date"
		self._assert_comment_is_invalid()

	def test_comment_with_invalid_user_is_invalid(self):
		self.comment.user = None
		self._assert_comment_is_invalid()

	def _assert_comment_is_valid(self):
		try:
			self.comment.full_clean()
		except ValidationError:
			self.fail("Comment object should be valid")

	def _assert_comment_is_invalid(self):
		with self.assertRaises(ValidationError):
			self.comment.full_clean()
