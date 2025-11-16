from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Recipe
from django.http import HttpResponse, Http404, HttpResponseRedirect

@login_required
def get_recipe(request, recipe_id):
    try:
        context = {'recipe': Recipe.objects.get(id=recipe_id)}
    except Recipe.DoesNotExist:
        raise Http404("Book not found.")
    return render(request, "specific_recipe.html", context)