from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.recipe_ingredient_form import RecipeIngredientForm

@login_required
def create_recipe_ingredient(request):
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()
            return redirect('dashboard')
    else:
        form = RecipeIngredientForm()
    return render(request, 'create_recipe_ingredient.html', {'form': RecipeIngredientForm})