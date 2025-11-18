from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.recipe_form import RecipeForm

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user 
            recipe.save()
            return redirect('dashboard')
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})