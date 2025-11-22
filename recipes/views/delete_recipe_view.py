from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

from recipes.models import Recipe

@login_required
@require_POST
def delete_recipe(request, recipe_id):
    current_user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if current_user == recipe.user:
        recipe.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    return HttpResponseForbidden("You are not allowed to delete this recipe.")