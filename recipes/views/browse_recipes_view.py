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
    if request.method == "POST":
        return redirect_with_params(request)

    recipe_list = get_base_queryset(request)
    form, search_val, tag_ids, ingredient_ids, order_by = get_params(request)

    recipe_list = apply_filters(recipe_list, search_val, tag_ids, ingredient_ids, order_by)

    page_obj = paginate_queryset(recipe_list, request.GET.get('page'))

    return render(request, 'all_recipes.html', {
        'recipe_list': recipe_list,
        'page_obj': page_obj,
        'search_val': search_val,
        'form': form
    })

def redirect_with_params(request):
    form = SearchRecipesForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(reverse('all_recipes'))

    params = build_query_params(
        form.cleaned_data['search_field'],
        form.cleaned_data['tags'],
        form.cleaned_data['order_by'],
        form.cleaned_data['ingredients']
    )
    return HttpResponseRedirect(reverse('all_recipes') + params)


def get_params(request):
    search_val = request.GET.get('search_val', '')
    tag_ids = [int(t) for t in request.GET.get('tags', '').split(',') if t]
    ingredient_ids = [int(i) for i in request.GET.get('ingredients', '').split(',') if i]
    order_by = request.GET.get('order_by', '')

    form = SearchRecipesForm(initial={
        'search_field': search_val,
        'tags': tag_ids,
        'ingredients': ingredient_ids,
        'order_by': order_by
    })
    return form, search_val, tag_ids, ingredient_ids, order_by


def build_query_params(search_val, tags, order_by, ingredients):
    params = []
    if search_val:
        params.append(f"search_val={search_val}")
    if tags:
        params.append("tags=" + ",".join(str(t.id) for t in tags))
    if order_by:
        params.append(f"order_by={order_by}")
    if ingredients:
        params.append("ingredients=" + ",".join(str(i.id) for i in ingredients))
    return "?" + "&".join(params) if params else ""

def get_base_queryset(request):
    return Recipe.objects.filter(
        Q(public=True) |
        Q(user__followers=request.user) |
        Q(user=request.user)
    ).distinct()


def apply_filters(qs, search_val, tag_ids, ingredient_ids, order_by):
    if search_val:
        qs = qs.filter(title__icontains=search_val)
    if tag_ids:
        qs = qs.filter(tags__id__in=tag_ids).distinct()
    if ingredient_ids:
        recipe_ids = get_recipes_by_ingredients(ingredient_ids)
        qs = qs.filter(id__in=recipe_ids)
    return apply_ordering(qs, order_by)


def get_recipes_by_ingredients(ingredient_ids):
    return RecipeIngredient.objects.filter(
        ingredient__in=ingredient_ids
    ).values_list('recipe_id', flat=True).distinct()


def apply_ordering(qs, order_by):
    if not order_by:
        return qs.order_by('id')
    if order_by in ('favourites', '-favourites'):
        return order_by_favourites(qs, order_by)
    if order_by in ('rating', '-rating'):
        return order_by_rating(qs, order_by)
    return qs.order_by(order_by)


def order_by_favourites(qs, order_by):
    qs = qs.annotate(fav_count=Count('favourites'))
    return qs.order_by('-fav_count' if order_by == 'favourites' else 'fav_count')


def order_by_rating(qs, order_by):
    qs = qs.annotate(avg_rating=Avg('rating__rating'))
    return qs.order_by('-avg_rating' if order_by == 'rating' else 'avg_rating')


def paginate_queryset(qs, page_number):
    return Paginator(qs, 12).get_page(page_number)
