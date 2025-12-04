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

	if request.method == "POST":
		form = MethodStepForm(request.POST, instance=method_step)

		if form.is_valid():
			try:
				form.save()
			except Exception:
				raise Http404("It wasn't possible to save this step to the database")
			else:
				return HttpResponseRedirect(
					reverse('add_method', kwargs={'recipe_id':recipe.pk})
				)
	else:
		form = MethodStepForm(instance=method_step)

	context = {
	'recipe': recipe,
	'method_step': method_step,
	'form': form,
	}

	return render(request, 'edit_method_step.html', context)