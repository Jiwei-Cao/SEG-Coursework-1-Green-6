from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recipes.forms import MethodStepForm
from recipes.models import Recipe, MethodStep

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse


@login_required
def add_method(request, recipe_id):

	recipe = get_object_or_404(Recipe, id=recipe_id)
	if is_create_method_step_post(request):
		handle_create_method_step(request, recipe)
		return HttpResponseRedirect(request.path_info)
	elif is_delete_method_step_post(request):
		delete_method_step(request, recipe)
		return HttpResponseRedirect(request.path_info)
	elif is_get_edit_method_step_post(request):
		path = reverse('edit_method', kwargs={'recipe_id': recipe.pk, 'step_id' : request.POST.get('step_clicked')})
		return HttpResponseRedirect(path)
	#elif is_clear_method_post(request):
		#clear_method_steps(request, recipe)
		#return HttpResponseRedirect(request.path_info)
	

	form = MethodStepForm()

	context = {
	'recipe': recipe,
	'form': form,
	}

	return render(request, 'add_method.html', context)


def is_create_method_step_post(request):
	return request.method == "POST" and request.POST.get("operation") == "add_step"

def handle_create_method_step(request, recipe):
	form = MethodStepForm(request.POST)
	if (form.is_valid() and step_number_is_unique(request, recipe, form)):
		create_method_step(request, recipe, form)


def step_number_is_unique(request, recipe, form):
	if recipe.method_steps.filter(step_number=form.cleaned_data['step_number']).count() <= 0:
		return True
	else:
		return False

def create_method_step(request, recipe, form):
	try:
		method_step = MethodStep(step_number=form.cleaned_data['step_number'], method_text=form.cleaned_data['method_text'])
		method_step.save()
		recipe.method_steps.add(method_step)
	except:
		raise Http404("Couldn't create method step.")
		return HttpResponseNotFound()


def is_delete_method_step_post(request):
	return request.method == "POST" and request.POST.get("operation") == "delete_step"

def delete_method_step(request, recipe):
    try:
	    method_step = MethodStep.objects.get(pk=request.POST.get('step_clicked'))
	    recipe.method_steps.remove(method_step)
    except:
        raise Http404(f"Could not delete step")
        return HttpResponseNotFound()
    else: 
        method_step.delete()


def is_get_edit_method_step_post(request):
	return request.method == "POST" and request.POST.get("operation") == "edit_step"





#def clear_method_steps(request, recipe):
#def is_clear_method_steps_post(request):
	#return request.method == "POST" and request.POST.get("operation") == "clear_steps"