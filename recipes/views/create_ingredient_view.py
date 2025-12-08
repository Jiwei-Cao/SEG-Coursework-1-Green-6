from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.ingredient_form import IngredientForm

@login_required
def create_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST, request.FILES)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            form.save()
            return redirect('specify_ingredient')
    else:
        form = IngredientForm()
    context = {'form': form}    
    return render(request, 'specify_ingredient.html', context)