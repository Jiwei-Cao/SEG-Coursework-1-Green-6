from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from recipes.forms.user_ingredient_form import UserIngredientForm
from ..models import UserIngredient
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def cupboard(request):
    current_user = request.user
    if request.method == "POST":
        form = UserIngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.user = request.user
            ingredient.save()
            return redirect('cupboard')
        else:
            path = reverse('cupboard') 
            return HttpResponseRedirect(path)
    else:
        user_ingredients = UserIngredient.objects.all()
        ingredients_list = []
        for ingredient in user_ingredients:
            ingredient_line = str(ingredient)
            ingredients_dict = {"ingredient": ingredient, 
                                "ingredient_line": ingredient_line}
            ingredients_list.append(ingredients_dict)
        form = UserIngredientForm()

    context = {
        'form': form,
        'user': current_user,
        'ingredients_list': ingredients_list,
    }
    return render(request, 'cupboard.html', context)