from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


@login_required
def delete_method_step(request, recipe_id, step_id):
	"""Delete a method step and renumber the later steps."""
	recipe = get_object_or_404(Recipe, id=recipe_id)

	try:
		method_step = MethodStep.objects.get(pk=step_id)
	except Exception:
		raise Http404("Couldn't delete method step.")
	
	deleted_number = method_step.step_number
	recipe.method_steps.remove(method_step)
	method_step.delete()
	
	shift_steps_after_deleting(recipe, deleted_number)

	path = reverse('add_method', kwargs={'recipe_id': recipe.pk,})
	return HttpResponseRedirect(path)
	

def shift_steps_after_deleting(recipe, deleted_number):
	"""Shift later step numbers down after a number is removed."""
	later_steps = recipe.method_steps.filter(step_number__gt=deleted_number).order_by('step_number')

	for step in later_steps:
		step.step_number -= 1
		step.save() 
