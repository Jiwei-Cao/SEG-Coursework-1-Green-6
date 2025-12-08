from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse


@login_required
def add_method(request, recipe_id):

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
	form = MethodStepForm(request.POST)

	if form.is_valid():
		try:
			method_step = form.save(commit=False)

			last_step = recipe.method_steps.order_by('-step_number').first()

			# order the steps
			if last_step != None:
				next_number = last_step.step_number + 1
			else:
				next_number = 1
			
			method_step.step_number = next_number
			method_step.save()
			recipe.method_steps.add(method_step)
		except Exception:
			raise Http404("Couldn't create method step.")
		
	return HttpResponseRedirect(request.path_info)

