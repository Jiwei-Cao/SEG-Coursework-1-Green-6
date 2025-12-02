from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipes.forms.recipe_ingredient_form import RecipeIngredientFormSet
from recipes.models import Recipe, RecipeIngredient


@login_required
def manage_recipe_ingredient(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)

    if request.method == 'POST':
        recipe_ingredient_formset = RecipeIngredientFormSet(request.POST, request.FILES, prefix='recipe_ingredient')
        if recipe_ingredient_formset.is_valid():

            recipe_ingredient_forms = recipe_ingredient_formset.save(commit=False)
            for to_delete in recipe_ingredient_formset.deleted_objects:
                to_delete.delete()

            for recipe_ingredient in recipe_ingredient_forms:
                recipe_ingredient.recipe = recipe
                recipe_ingredient.user = request.user
                recipe_ingredient.save()
            path = reverse('manage_recipe_ingredient', kwargs={"recipe_id": f"{recipe.id}"}) 
            return redirect(path)

    else:
        recipe_ingredient_formset = RecipeIngredientFormSet(queryset=RecipeIngredient.objects.filter(recipe=recipe), prefix='recipe_ingredient')

    return render(request, 'create_recipe_ingredient.html', {'formset': recipe_ingredient_formset})
