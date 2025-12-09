from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from recipes.models import Recipe, MethodStep

@login_required
@require_POST
def delete_recipe(request, recipe_id):
    current_user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if current_user == recipe.user:
        delete_method_steps(recipe)
        recipe.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    return HttpResponseForbidden("You are not allowed to delete this recipe.")

def delete_method_steps(recipe):
    for method_step in recipe.method_steps.all():
        method_step.delete()

