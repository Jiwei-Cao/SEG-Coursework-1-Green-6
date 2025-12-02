from recipes.models import MethodStep, User
from django.test import TestCase
from django.core.exceptions import ValidationError

class MethodStepModelTestCase(TestCase):

	fixtures = ['recipes/tests/fixtures/default_user.json']

	def setUp(self):

		self.user = User.objects.get(username='@johndoe')
		self.client.login(username=self.user.username, password='Password123')

		self.step_number = 1
		self.method_text = "testing"

		self.method_step = MethodStep(step_number=self.step_number, method_text=self.method_text)
		self.method_step.save()

	def test_valid_method_step(self):
		self._assert_method_step_is_valid()

	def test_step_number_cannot_be_0(self):
		self.method_step.step_number = 0
		self._assert_method_step_is_invalid()

	def test_step_number_cannot_be_negative(self):
		self.method_step.step_number = -1
		self._assert_method_step_is_invalid()

	def test_step_number_cannot_be_21(self):
		self.method_step.step_number = 21
		self._assert_method_step_is_invalid()

	def test_step_number_can_be_20(self):
		self.method_step.step_number = 20
		self._assert_method_step_is_valid()

	def test_step_number_with_invalid_data_type(self):
		self.method_step.step_number = "not a number"
		self._assert_method_step_is_invalid()

	def test_method_text_cannot_be_blank(self):
		self.method_step.method_text = ''
		self._assert_method_step_is_invalid()

	def test_method_step_with_overly_long_method_text(self):
		self.method_step.step_number = 'x' * 300
		self._assert_method_step_is_invalid()


	def _assert_method_step_is_valid(self):
		try:
			self.method_step.full_clean()
		except ValidationError:
			self.fail("MethodStep object should be valid")

	def _assert_method_step_is_invalid(self):
		with self.assertRaises(ValidationError):
			self.method_step.full_clean()