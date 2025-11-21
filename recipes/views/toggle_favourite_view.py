from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.forms import FavouriteForm
from recipes.models import Recipe
from recipes.models import Favourite

@login_required
def toggle_favourite(request, recipe_id):
    print("toggle_favourite")
    current_user = request.user
    recipe = Recipe.objects.get(id = recipe_id)
    if (current_user in recipe.favourites.all()):
        recipe.favourites.remove(current_user)
    else:
        recipe.favourites.add(current_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER',f'recipe/{recipe_id}'))