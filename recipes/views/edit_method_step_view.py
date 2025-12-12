from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden
from django.urls import reverse



@login_required
def edit_method_step(request, recipe_id, step_id):
	'''Render the page to allow user to edit a method step'''
	recipe = get_object_or_404(Recipe, id=recipe_id)
	method_step = get_object_or_404(MethodStep, id=step_id)

	response = validate_request(request,recipe, method_step)
	if response:
		return response

	if request.method == "POST":
		form = MethodStepForm(request.POST, instance=method_step)
		redirect = handle_saving_changes_to_method_step(request, recipe, method_step, form)
	else:
		form = MethodStepForm(instance=method_step)
		redirect = None

	if redirect:
		return redirect

	context = {
	'recipe': recipe,
	'method_step': method_step,
	'form': form,
	}

	return render(request, 'edit_method_step.html', context)


def validate_request(request, recipe, method_step):
	if method_step not in recipe.method_steps.all():
		raise Http404("Could not find the specified step under the chosen recipe")
	elif request.user != recipe.user:
		return HttpResponseForbidden("You are not authorised to edit this method step.")


def handle_saving_changes_to_method_step(request, recipe, method_step, form):
	''' Check if the edited form is valid before saving to the database'''
	if form.is_valid():
		form.save()
		return HttpResponseRedirect( reverse('add_method', kwargs={'recipe_id':recipe.pk}) )

	