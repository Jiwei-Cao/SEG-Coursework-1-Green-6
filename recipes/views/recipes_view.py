from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import Recipe
from recipes.forms import SearchRecipesForm
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def all_recipes(request):
    current_user = request.user
    if request.method == "POST":
        form = SearchRecipesForm(request.POST)
        if form.is_valid():
            try:
                search_val = f'?search_val={form.cleaned_data['search_field']}'
            except:
                form.add_error(None, "It wasn't possible to complete this search")
                search_val = ''
            else:
                path = reverse('all_recipes') + search_val
                return HttpResponseRedirect(path)

        else:
            path = reverse('all_recipes') 
            return HttpResponseRedirect(path)

    else:  
        search_val = request.GET.get('search_val', '')
        if search_val != '':
            recipes = Recipe.objects.filter(title__contains=search_val)
        else:
            recipes = Recipe.objects.all()
        
    return render(request, 'all_recipes.html', {
        'user': current_user,
        'recipes': recipes
    })
