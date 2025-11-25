from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from django.db.models import Q
from django.core.paginator import Paginator

from django.http import HttpResponseRedirect, Http404, HttpResponseNotFound
from django.urls import reverse

from recipes.forms import SearchRecipesForm
from recipes.models import Recipe


@login_required
def browse_recipes(request):
    recipe_list = Recipe.objects.filter(Q(public=True)|Q(user__followers=request.user)|Q(user=request.user)).distinct()
    if request.method == "POST":
        form = SearchRecipesForm(request.POST)
        if form.is_valid():
            search_val = form.cleaned_data['search_field']
            selected_tags = form.cleaned_data['tags']
            order_by = form.cleaned_data['order_by']

            params = []
            if search_val:
                params.append(f'search_val={search_val}')
            if selected_tags:
                tag_ids = ','.join(str(tag.id) for tag in selected_tags)
                params.append(f'tags={tag_ids}')
            if order_by:
                params.append(f'order_by={order_by}')
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
        form = SearchRecipesForm(initial=initial_data)

        if search_val != '':
            recipe_list = recipe_list.filter(title__contains=search_val)

        if tag_ids:
            recipe_list = recipe_list.filter(tags__id__in=tag_ids).distinct()

        if order_by:
            if order_by == 'favourites' or order_by == '-favourites':
                recipe_list = recipe_list.annotate(fav_count = Count('favourites'))
                if order_by == 'favourites':
                    recipe_list = recipe_list.order_by('fav_count')
                else:
                    recipe_list = recipe_list.order_by('-fav_count')
            else:
                recipe_list = recipe_list.order_by(order_by)
        else:
            recipe_list = recipe_list.order_by('id')

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