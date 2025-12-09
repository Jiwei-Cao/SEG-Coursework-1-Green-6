from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


@login_required
def add_method(request, recipe_id):
	"""Show the method-step editor for a recipe and handle the POST actions."""

	recipe = get_object_or_404(Recipe, id=recipe_id)

	if request.method == "POST":
		return handle_create_method_step(request, recipe)
		
	form = MethodStepForm()
	context = {
		'recipe': recipe, 
		'form': form
	}

	return render(request, 'add_method.html', context)


def handle_create_method_step(request, recipe):
	"""Create a new method for the recipe."""
	form = MethodStepForm(request.POST)

	invalid_response = check_valid_form(request, form, recipe)

	if invalid_response is not None:
		return invalid_response

	create_step_from_form(form, recipe)
		
	return HttpResponseRedirect(request.path_info)

def check_valid_form(request, form, recipe):
	"""Return the form with errors if the validation fails."""
	if not form.is_valid():
		return render(request, 'add_method.html', {
			'recipe': recipe,
			'form': form
		})
	
	return None
	
def update_last_number(last_step):
	"""Calculate the next step number after the last existing number."""
	if last_step != None:
		return last_step.step_number + 1
	
	return 1

def create_step_from_form(form, recipe):
	"""Save a new method step and attach it to the recipe."""
	try:
		method_step = form.save(commit=False)
		last_step = recipe.method_steps.order_by('-step_number').first()
		next_number = update_last_number(last_step)	
		method_step.step_number = next_number
		method_step.save()
		recipe.method_steps.add(method_step)
	except Exception:
		raise Http404("Couldn't create method step.")


