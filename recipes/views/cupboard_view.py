from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.ingredient_form import IngredientForm
from ..models import Ingredient
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def cupboard(request):
    current_user = request.user
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            return redirect('cupboard')
        else:
            path = reverse('cupboard') 
            return HttpResponseRedirect(path)
    else:
        ingredients = Ingredient.objects.all()
        form = IngredientForm()


    context = {
        'form': form,
        'user': current_user,
        'ingredients': ingredients
    }
    return render(request, 'cupboard.html', context)