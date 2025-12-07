from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse


@login_required
def add_method(request, recipe_id):
	recipe = get_object_or_404(Recipe, id=recipe_id)
	result = check_post_request(request, recipe)

	if result is not None:
		return result
		
	form = MethodStepForm()
	context = {
		'recipe': recipe, 
		'form': form
	}

	return render(request, 'add_method.html', context)

def check_post_request(request, recipe):
	if request.method != "POST":
		return None

	operation = request.POST.get("operation")

	if operation == "add_step":
		return handle_create_method_step(request, recipe)
	elif operation == "delete_step":
		return handle_delete_method_step(request, recipe)
	elif operation == "edit_step":
		step_id = request.POST.get('step_clicked')
		path = reverse('edit_method_step', kwargs={'recipe_id': recipe.pk, 'step_id': step_id})
		return HttpResponseRedirect(path)

	return None

def handle_create_method_step(request, recipe):
	form = MethodStepForm(request.POST)

	invalid_response = check_valid_form(request, form, recipe)

	if invalid_response is not None:
		return invalid_response

	create_step_from_form(form, recipe)
		
	return HttpResponseRedirect(request.path_info)

def check_valid_form(request, form, recipe):
	if not form.is_valid():
		return render(request, 'add_method.html', {
			'recipe': recipe,
			'form': form
		})
	
	return None
	
def update_last_number(last_step):
	if last_step != None:
		return last_step.step_number + 1
	
	return 1

def create_step_from_form(form, recipe):
	try:
		method_step = form.save(commit=False)
		last_step = recipe.method_steps.order_by('-step_number').first()
		next_number = update_last_number(last_step)	
		method_step.step_number = next_number
		method_step.save()
		recipe.method_steps.add(method_step)
	except Exception:
		raise Http404("Couldn't create method step.")

def handle_delete_method_step(request, recipe):
	step_id = request.POST.get('step_clicked')

	try:
		method_step = recipe.method_steps.get(pk=step_id)
	except Exception:
		raise Http404("Couldn't delete method step.")
	
	deleted_number = method_step.step_number
	method_step.delete()

	shift_steps_after_deleting(recipe, deleted_number)

	return HttpResponseRedirect(request.path_info)

def shift_steps_after_deleting(recipe, deleted_number):
	later_steps = recipe.method_steps.filter(step_number__gt=deleted_number).order_by('step_number')

	for step in later_steps:
		step.step_number -= 1
		step.save() 