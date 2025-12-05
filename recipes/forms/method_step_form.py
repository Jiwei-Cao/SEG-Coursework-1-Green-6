from django import forms
from recipes.models import MethodStep

class MethodStepForm(forms.ModelForm):
	class Meta:
		model = MethodStep
		fields = ['method_text']