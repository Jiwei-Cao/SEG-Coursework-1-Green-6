from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import Comment

import datetime
from django.utils.timezone import make_aware

class DeleteCommentViewTestCase(TestCase):
	'''Tests for the delete_comment view '''
	
	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		
		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123")
		self.test_comment = Comment.objects.create(user=self.user, comment="test comment", date_published=make_aware(datetime.datetime(2025,4,1)))
		self.recipe1.comments.add(self.test_comment)

		self.url = reverse("delete_comment", kwargs={'recipe_id': self.recipe1.pk, 'comment_id': self.test_comment.pk})


		
	def test_delete_comment_url(self):
		self.assertEqual(self.url, f"/recipe/{self.recipe1.pk}/comment/{self.test_comment.pk}/delete_comment")

	def test_get_delete_comment(self):
		response = self.client.get(self.url, follow=True)
		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

	def test_get_delete_comment_with_invalid_recipe_pk(self): 
		invalid_url = reverse('delete_comment', kwargs= {'recipe_id' : '5', 'comment_id': 1})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_get_delete_comment_with_invalid_comment_pk(self): 
		invalid_url = reverse('delete_comment', kwargs= {'recipe_id' : self.recipe1.pk, 'comment_id': 9})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_delete_valid_comment(self):		
		before_comment_objects_count = Comment.objects.count()
		before_recipe_comments_count = self.recipe1.comments.all().count()
		response = self.client.post(self.url, follow=True)
		after_comment_objects_count = Comment.objects.count()
		after_recipe_comments_count = self.recipe1.comments.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count-1)
		self.assertEqual(after_recipe_comments_count, before_recipe_comments_count-1)

		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

		try:
				deleted_comment = Comment.objects.get(pk=self.test_comment.pk)
		except Comment.DoesNotExist:
			pass
		else:
			self.fail("Comment should've been removed after deletion")

		try:
			deleted_recipe_comment = self.recipe1.comments.get(pk=self.test_comment.pk)
		except Comment.DoesNotExist:
			pass
		else:
			self.fail("Comment should've been removed after deletion")

	def test_delete_comment_with_invalid_comment_pk(self):

		invalid_url = reverse('delete_comment', kwargs= {'recipe_id' : self.recipe1.pk, 'comment_id': 5})
		before_comment_objects_count = Comment.objects.count()
		before_recipe_comments_count = self.recipe1.comments.all().count()

		response = self.client.post(invalid_url, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_recipe_comments_count = self.recipe1.comments.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_recipe_comments_count, before_recipe_comments_count)

		self.assertEqual(response.status_code, 404)

	def test_delete_comment_with_invalid_recipe_pk(self):

		invalid_url = reverse('delete_comment', kwargs= {'recipe_id' : 9, 'comment_id': self.test_comment.pk})
		before_comment_objects_count = Comment.objects.count()
		before_recipe_comments_count = self.recipe1.comments.all().count()

		response = self.client.post(invalid_url, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_recipe_comments_count = self.recipe1.comments.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_recipe_comments_count, before_recipe_comments_count)

		self.assertEqual(response.status_code, 404)

	def test_delete_comment_deletes_replies(self):
		second_comment = Comment.objects.create(user=self.user, comment="second comment", date_published=make_aware(datetime.datetime(2025,3,1)))
		reply = Comment.objects.create(user=self.user, comment="test reply", date_published=make_aware(datetime.datetime(2025,9,1)))
		self.test_comment.replies.add(reply)

		before_comment_objects_count = Comment.objects.count()
		comment_reply_count = self.test_comment.replies.count() 
		response = self.client.post(self.url, follow=True)
		after_comment_objects_count = Comment.objects.count()
		self.assertEqual(after_comment_objects_count, before_comment_objects_count - (comment_reply_count + 1))

		try:
				deleted_comment = Comment.objects.get(pk=self.test_comment.pk)
		except Comment.DoesNotExist:
			pass
		else:
			self.fail("Comment should've been removed after deletion")

		try:
				deleted_reply = Comment.objects.get(pk=reply.pk)
		except Comment.DoesNotExist:
			pass
		else:
			self.fail("Reply should've been removed after deletion")



