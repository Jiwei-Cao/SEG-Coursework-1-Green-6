from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse


@login_required
def edit_method_step(request, recipe_id, step_id):

	recipe = get_object_or_404(Recipe, id=recipe_id)
	method_step = get_object_or_404(MethodStep, id=step_id)
	
	if is_save_changes_post(request):
		handle_save_edit_changes(request, recipe, method_step)
		path = reverse('add_method', kwargs={'recipe_id':recipe.pk})
		return HttpResponseRedirect(path)

	form = MethodStepForm(instance=method_step)

	context = {
	'recipe': recipe,
	'method_step': method_step,
	'form': form,
	}


	return render(request, 'edit_method_step.html', context)

def is_save_changes_post(request):
	return request.method == "POST" and request.POST.get('operation') == "save_changes"

def handle_save_edit_changes(request, recipe, method_step):
	form = MethodStepForm(request.POST, instance=method_step)
	
	if form.is_valid() and check_step_number_is_unique(request, recipe, method_step, form):
		save_changes(request,method_step, form)

def save_changes(request, method_step, form):
	try: 
		form.save()
	except:
		form.add_error(None, "It wasn't possible to save this step to the database")

def check_step_number_is_unique(request, recipe, method_step, form):
	temp_method_steps = recipe.method_steps.filter(step_number=form.cleaned_data['step_number'])
	if temp_method_steps.count() == 0:
		return True
	elif temp_method_steps.count() == 1: 
		return check_step_number_that_exists_is_the_one_edited(temp_method_steps, method_step )

def check_step_number_that_exists_is_the_one_edited(temp_method_steps, method_step):
	try:
		temp_method_steps.get(pk=method_step.pk)
		return True
	except: 
		return False