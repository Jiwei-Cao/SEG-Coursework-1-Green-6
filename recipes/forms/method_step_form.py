from django import forms
from recipes.models import MethodStep

class MethodStepForm(forms.ModelForm):
	'''Form used to allow a user to create a method step'''
	class Meta:
		model = MethodStep
		fields = ['method_text']
		