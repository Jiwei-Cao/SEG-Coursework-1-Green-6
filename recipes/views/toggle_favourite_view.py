from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.forms import FavouriteForm
from recipes.models import Recipe
from recipes.models import Favourite

@login_required
@require_POST
def toggle_favourite(request, recipe_id):
    current_user = request.user
    recipe = get_object_or_404(Recipe,id = recipe_id)
    if (current_user in recipe.favourites.all()):
        recipe.favourites.remove(current_user)
    else:
        recipe.favourites.add(current_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER',f'recipe/{recipe_id}'))