from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count, Avg, Q
from django.core.paginator import Paginator

from django.http import HttpResponseRedirect
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe, RecipeIngredient


@login_required
def browse_recipes(request):
    recipe_list = Recipe.objects.filter(Q(public=True)|Q(user__followers=request.user)|Q(user=request.user)).distinct()
    if request.method == "POST":
        form = SearchRecipesForm(request.POST)
        if form.is_valid():
            search_val = form.cleaned_data['search_field']
            selected_tags = form.cleaned_data['tags']
            order_by = form.cleaned_data['order_by']
            ingredient_ids_as_str = form.cleaned_data['ingredients']

            params = []
            if search_val:
                params.append(f'search_val={search_val}')
            if selected_tags:
                tag_ids = ','.join(str(tag.id) for tag in selected_tags)
                params.append(f'tags={tag_ids}')
            if order_by:
                params.append(f'order_by={order_by}')
            if ingredient_ids_as_str:
                ingredient_ids_as_str = ','.join(str(ingredient.id) for ingredient in ingredient_ids_as_str)
                params.append(f'ingredients={ingredient_ids_as_str}')

            query = '?' + '&'.join(params) if params else ''
            
            path = reverse('all_recipes') + query
            return HttpResponseRedirect(path)
        else:
            return HttpResponseRedirect(reverse('all_recipes'))
    else:
        search_val = request.GET.get('search_val', '')
        tag_ids = request.GET.get('tags','')
        initial_data = {'search_field': search_val}
        order_by = request.GET.get('order_by','')
        initial_data['order_by'] = order_by
        if tag_ids:
            tag_ids = [int (tag_id) for tag_id in tag_ids.split(',')]
            initial_data['tags'] = tag_ids

        ingredient_ids_as_str = request.GET.get('ingredients', '')
        if ingredient_ids_as_str:
            ingredient_ids = [int (ingredient_id) for ingredient_id in ingredient_ids_as_str.split(',')]
            initial_data['ingredients'] = ingredient_ids

        form = SearchRecipesForm(initial=initial_data)

        if search_val != '':
            recipe_list = recipe_list.filter(title__contains=search_val)

        if tag_ids:
            recipe_list = recipe_list.filter(tags__id__in=tag_ids).distinct()

        recipe_list = check_order_by(order_by, recipe_list)

        if ingredient_ids_as_str != '':
            # Get ALL recipe ids that match the ingredients that are being searched for
            recipe_ids_by_ingredients = generate_recipe_ids_by_ingredients(ingredient_ids_as_str)
            #Filter the list so far by the recipe ids from the previous call; this acts like an intersection of sets
            recipe_list = recipe_list.filter(id__in=recipe_ids_by_ingredients)

    paginator = Paginator(recipe_list, 12)
    page_number =request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipe_list': recipe_list,
        'page_obj': page_obj,
        'search_val': search_val,
        'form' : form
    }

    return render(request, 'all_recipes.html', context)


def generate_recipe_ids_by_ingredients(str_ingredient_ids):
    ingredient_ids = [int(ingredient_id) for ingredient_id in str_ingredient_ids.split(',')]
    filtered_recipe_ingredients = RecipeIngredient.objects.filter(ingredient__in=ingredient_ids)
    filtered_recipe_ids = []
    for ingredient in filtered_recipe_ingredients:
        filtered_recipe_ids.append(ingredient.recipe.id)
    return filtered_recipe_ids

def add_params(search_val, selected_tags, order_by, searched_ingredients):
    params = []
    if search_val:
        params.append(f'search_val={search_val}')
    if selected_tags:
        tag_ids = ','.join(str(tag.id) for tag in selected_tags)
        params.append(f'tags={tag_ids}')
    if order_by:
        params.append(f'order_by={order_by}')
    if searched_ingredients:
        params.append(f'ingredients={searched_ingredients}')
    return '?' + '&'.join(params) if params else ''

def check_order_by(order_by,recipe_list):
    if order_by:
        print(order_by)
        recipe_list = check_order_by_type(order_by, recipe_list)
    else:   
        recipe_list = recipe_list.order_by('id')
    return recipe_list

def check_order_by_type(order_by, recipe_list):
    if order_by == 'favourites' or order_by == '-favourites':
        recipe_list = recipe_list.annotate(fav_count = Count('favourites'))
        if order_by == 'favourites':
            recipe_list = recipe_list.order_by('fav_count')
        else:
            recipe_list = recipe_list.order_by('-fav_count')
    elif order_by == "rating" or order_by == "-rating":
        recipe_list = recipe_list.annotate(avg_rating=Avg('rating__rating'))
        recipe_list = recipe_list.order_by('-avg_rating' if order_by == 'rating' else 'avg_rating')
    else:
        recipe_list = recipe_list.order_by(order_by)
    return recipe_list
