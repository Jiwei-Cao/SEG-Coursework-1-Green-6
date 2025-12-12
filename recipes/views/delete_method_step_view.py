from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse


@login_required
def handle_delete_method_step(request, recipe_id, step_id):
	"""Handles POST requests and redirects user to method page"""

	recipe = get_object_or_404(Recipe, id=recipe_id)
	if request.user != recipe.user:
		return HttpResponseForbidden("You are not authorised to delete this method step.")
	elif request.method == "POST":
		delete_method_step(request, recipe, step_id)

	path = reverse('add_method', kwargs={'recipe_id': recipe.pk,})
	return HttpResponseRedirect(path)
	

def delete_method_step(request, recipe, step_id):
	"""Delete a method step and renumber the later steps."""
	try:
		method_step = MethodStep.objects.get(pk=step_id)
	except Exception:
		raise Http404("Couldn't delete method step.")
	
	if method_step not in recipe.method_steps.all():
		raise Http404("Could not find the specified step under the chosen recipe")

	deleted_number = method_step.step_number
	recipe.method_steps.remove(method_step)
	method_step.delete()
	shift_steps_after_deleting(recipe, deleted_number)


def shift_steps_after_deleting(recipe, deleted_number):
	"""Shift later step numbers down after a number is removed."""
	later_steps = recipe.method_steps.filter(step_number__gt=deleted_number).order_by('step_number')

	for step in later_steps:
		step.step_number -= 1
		step.save() 

