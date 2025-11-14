from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe


@login_required
def browse_recipes(request):

    if request.method == "POST":
        form = SearchRecipesForm(request.POST)
        if form.is_valid():
            try:
                #recipe_list = (6,7,8)
                #recipe_list = Recipe.objects.filter(title__contains=form.cleaned_data['search_field'])
                search_val = f'?search_val={form.cleaned_data['search_field']}'
            except:
                form.add_error(None, "It wasn't possible to complete this search")
                search_val = ''
            else:
                path = reverse('browse_recipes') + search_val
                return HttpResponseRedirect(path)

        else:
            #recipe_list = Recipe.objects.all()
            #recipe_list = (1,2,3)
            path = reverse('browse_recipes') 
            return HttpResponseRedirect(path)

    else:  
        search_val = request.GET.get('search_val', '')
        if search_val != '':
            #recipe_list = (6,7,8)
            recipe_list = Recipe.objects.filter(title__contains=search_val)
        else:
            #recipe_list = (1,2,3)
            recipe_list = Recipe.objects.all()
        

    
    context = {'recipe_list' : recipe_list}
    
    return render(request, 'browse_recipes.html', context)
