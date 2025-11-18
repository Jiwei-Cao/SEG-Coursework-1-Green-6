from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.forms import FavouriteForm
from recipes.models import Recipe
from recipes.models import Favourite


@login_required
def browse_recipes(request):
    recipe_list = Recipe.objects.all()
    if request.method == "POST":
        
        if request.POST.get('form_type') == 'favourite_form':
            search_val = handle_favourites_form_requests(request)
            path = reverse('browse_recipes') + search_val

            return HttpResponseRedirect(path)
            
        elif request.POST.get('form_type') == 'search_form' :
            form = SearchRecipesForm(request.POST)
            if form.is_valid():
                try:
                    search_val = f'?search_val={form.cleaned_data['search_field']}'
                except:
                    form.add_error(None, "It wasn't possible to complete this search")
                    search_val = ''

                else:
                    path = reverse('browse_recipes') + search_val
                    return HttpResponseRedirect(path)

            else:
                path = reverse('browse_recipes') 
                return HttpResponseRedirect(path)
        else:
            search_val = ''
            form = None

    else:  
        form = SearchRecipesForm()
        search_val = request.GET.get('search_val', '')
        
        if search_val != '':
            recipe_list = Recipe.objects.filter(title__contains=search_val)
        else:
            recipe_list = Recipe.objects.all()
        
        

    favourited_recipe_ids = Favourite.objects.filter(user=request.user).values_list('recipe', flat=True)
    recipe_favourite_counts = map_recipe_to_favourite_count()
    user_favourite_objects = Favourite.objects.filter(user=request.user)

    context = {
    'recipe_list': recipe_list,
    'search_val': search_val,
    'user_favourite_objects': user_favourite_objects, 
    'user_favourited_recipe_ids': favourited_recipe_ids, 
    'single_recipe_favourites_count': recipe_favourite_counts,
    'form' : form
    }

    return render(request, 'browse_recipes.html', context)


def handle_favourites_form_requests(request):
    if request.POST.get('favourite_recipe', '') == 'unfavourite_recipe':
        unfavourite_recipe(request)
    elif request.POST.get('favourite_recipe', '') == 'favourite_recipe':
        favourite_recipe(request)

    search_val = request.POST.get('search_val', '')
    search_query_string = f'?search_val={search_val}'
    if search_val == '' :
        search_query_string = ''

    return search_query_string


def favourite_recipe(request):

    form = FavouriteForm(request.POST)

    try:
        current_user = request.user
        recipe_clicked = Recipe.objects.get(pk=(request.POST.get("recipe_clicked")))
        favourite = Favourite(user=current_user, recipe=recipe_clicked)
        favourite.save() 
    except:
        form.add_error(None, " Couldn't favourite this recipe") 

    return render(request, 'browse_recipes.html')


def unfavourite_recipe(request):

    try:
        favourite = Favourite.objects.filter(user=request.user, recipe=request.POST.get("recipe_clicked"))
    except Favourite.DoesNotExist:
        raise Http404(f"Could not unfavourite recipe")
        return HttpResponseNotFound()
    else: 
        favourite.delete()

    return render(request, 'browse_recipes.html')

    

def map_recipe_to_favourite_count():
    favourite_count_on_recipes = []
    for recipe in Recipe.objects.all():
        count = Favourite.objects.filter(recipe=recipe.pk).count()
        favourite_count_on_recipes.append((recipe.pk, count))

    return favourite_count_on_recipes
