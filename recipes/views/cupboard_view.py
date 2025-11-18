from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.ingredient_form import IngredientForm

@login_required
def cupboard(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            return redirect('dashboard')
    else:
        form = IngredientForm()
    context = {
        'form': form
        }

    return render(request, 'cupboard.html', context)