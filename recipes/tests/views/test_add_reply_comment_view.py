from django.test import TestCase

from django.urls import reverse

from recipes.models import Recipe
from recipes.models import User
from recipes.models import Comment

import datetime
from django.utils.timezone import make_aware

class AddReplyCommentViewTestCase(TestCase):
	'''Tests for the add_reply_comment view '''
	
	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):
		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')
		
		self.recipe1 =  Recipe.objects.create(user=self.user, title="123",description="123")
		self.parent_comment = Comment.objects.create(user=self.user, comment="test comment", date_published=make_aware(datetime.datetime(2025,4,1)))

		self.url = reverse("add_reply_comment", kwargs={'recipe_id': self.recipe1.pk, 'parent_comment_id' : self.parent_comment.pk})

		self.form_input = {
				'comment': 'testing',
		}

	def test_add_reply_comment_url(self):
		self.assertEqual(self.url, f"/recipe/{self.recipe1.pk}/comment/{self.parent_comment.pk}/reply")

	def test_get_add_reply_comment(self):
		response = self.client.get(self.url, follow=True)
		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

	def test_get_add_reply_comment_with_invalid_recipe_pk(self): 
		invalid_url = reverse('add_reply_comment', kwargs= {'recipe_id' : '5', 'parent_comment_id' : self.parent_comment.pk})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_get_add_reply_comment_with_invalid_parent_comment_pk(self): 
		invalid_url = reverse('add_reply_comment', kwargs= {'recipe_id' : self.recipe1.pk, 'parent_comment_id' : 6})
		response = self.client.post(invalid_url, follow=True)
		self.assertEqual(response.status_code, 404)

	def test_create_reply_comment_with_valid_data(self):
		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(self.url, self.form_input, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count + 1)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count + 1)

		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

	
	def test_create_reply_comment_with_blank_text(self):
		self.form_input['comment'] = ''

		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(self.url, self.form_input, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count)

		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)


	def test_create_reply_comment_with_overly_long_text(self):
		self.form_input['comment'] = 'x'*600

		before_comment_objects_count = Comment.objects.count()
		before_comment_replies_count = self.parent_comment.replies.all().count()
		response = self.client.post(self.url, self.form_input, follow=True)

		after_comment_objects_count = Comment.objects.count()
		after_comment_replies_count = self.parent_comment.replies.all().count()

		self.assertEqual(after_comment_objects_count, before_comment_objects_count)
		self.assertEqual(after_comment_replies_count, before_comment_replies_count)

		expected_redirect_url = reverse("get_recipe",  kwargs={"recipe_id": f"{self.recipe1.pk}"})
		self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)

	
