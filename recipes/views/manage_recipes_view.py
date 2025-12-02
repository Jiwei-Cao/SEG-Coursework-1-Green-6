from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from recipes.models import Recipe

@login_required
def manage_recipes(request):
    recipe_list = Recipe.objects.all()
    return render(request, 'manage_recipes.html', {'recipe_list': recipe_list})
