from django import forms
from recipes.models import MethodStep

class MethodStepForm(forms.ModelForm):
	class Meta:
		model = MethodStep
		fields = ['step_number', 'method_text']