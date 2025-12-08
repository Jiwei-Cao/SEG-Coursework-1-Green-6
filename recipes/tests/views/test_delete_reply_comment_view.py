from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import Comment

import datetime
from django.utils.timezone import make_aware

class DeleteReplyCommentViewTestCase(TestCase):
	'''Tests for the delete_reply_comment view '''
	
	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		
		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123")
		self.parent_comment = Comment.objects.create(user=self.user, comment="test comment", date_published=make_aware(datetime.datetime(2025,4,1)))
		self.recipe1.comments.add(self.parent_comment)

		self.reply_comment = Comment.objects.create(user=self.user, comment="test reply", date_published=make_aware(datetime.datetime(2025,8,1)))
		self.parent_comment.replies.add(self.reply_comment)

		self.url = reverse("delete_reply_comment", kwargs={'recipe_id': self.recipe1.pk, 'parent_comment_id' : self.parent_comment.pk, 'reply_comment_id': self.reply_comment.pk})

	def test_delete_reply_comment_url(self):
		self.assertEqual(self.url, f"/recipe/{self.recipe1.pk}/comment/{self.parent_comment.pk}/delete_reply_comment/{self.reply_comment.pk}")

	def test_get_delete_reply_comment(self):
		response = self.client.get(self.url, follow=True)
		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

	def test_get_delete_reply_comment_with_invalid_recipe_pk(self): 
		invalid_url = reverse('delete_reply_comment', kwargs= {'recipe_id' : '5', 'parent_comment_id' : self.parent_comment.pk, 'reply_comment_id':self.reply_comment.pk})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_get_delete_reply_comment_with_invalid_parent_comment_pk(self): 
		invalid_url = reverse('delete_reply_comment', kwargs= {'recipe_id' : self.recipe1.pk, 'parent_comment_id' : 6, 'reply_comment_id':self.reply_comment.pk})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_delete_valid_reply_comment(self):

		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(self.url, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count-1)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count-1)

		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		try:
				deleted_reply = Comment.objects.get(pk=self.reply_comment.pk)
				deleted_comment_reply = self.parent_comment.replies.get(pk=reply.pk)
		except Comment.DoesNotExist:
			pass
		else:
			self.fail("Reply should've been removed after deletion")

	def test_delete_reply_comment_with_invalid_pk(self):
		invalid_url = reverse('delete_reply_comment', kwargs= {'recipe_id' : self.recipe1.pk, 'parent_comment_id' : self.parent_comment.pk, 'reply_comment_id': 7})
		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(invalid_url,  follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count)

		self.assertEqual(response.status_code, 404)

	def test_delete_reply_comment_with_invalid_recipe_pk(self):
		invalid_url = reverse('delete_reply_comment', kwargs= {'recipe_id' : 8, 'parent_comment_id' : self.parent_comment.pk, 'reply_comment_id': self.reply_comment.pk})
		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(invalid_url, follow=True)

		after_comment_objects_count = Comment.objects.count()

		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count)

		self.assertEqual(response.status_code, 404)


