from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipes.forms import RecipeForm

@login_required
def create_recipe(request):
    """Displays the recipe form when it's GET, handles recipe creation when it's POST."""
    if request.method != 'POST':
        form = RecipeForm()
        return render(request, 'create_recipe.html', {'form': form})
    
    form = RecipeForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(request, 'create_recipe.html', {'form': form})

    path = save_recipe_from_form(request, form)

    return redirect(path)

def save_recipe_from_form(request, form):
    """Create and save a recipe instance from the form and return the redirect URL."""
    recipe = form.save(commit=False)
    recipe.user = request.user 
    recipe.save()
    form.save_m2m()
    
    return reverse('add_method', kwargs={"recipe_id": f"{recipe.id}"}) 