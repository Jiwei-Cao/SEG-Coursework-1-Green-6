from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from recipes.forms import RecipeForm

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user 
            recipe.save()
            form.save_m2m()
            path = reverse('add_method', kwargs={"recipe_id": f"{recipe.id}"}) 
            return redirect(path)
    else:
        form = RecipeForm()

    return render(request, 'create_recipe.html', {'form': form})