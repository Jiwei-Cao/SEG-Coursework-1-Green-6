from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.recipe_method_form import RecipeMethodForm

@login_required
def create_recipe_method(request):
    if request.method == 'POST':
        form = RecipeMethodForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()
            return redirect('create_recipe_method')
    else:
        form = RecipeMethodForm()
    return render(request, 'create_recipe_method.html', {'form': RecipeMethodForm})