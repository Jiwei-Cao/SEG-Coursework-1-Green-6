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
                search_val = form.cleaned_data['search_field']
                selected_tags = form.cleaned_data['tags']

                params = []
                if search_val:
                    params.append(f'search_val={search_val}')
                if selected_tags:
                    tag_ids = ','.join(str(tag.id) for tag in selected_tags)
                    params.append(f'tags={tag_ids}')
                query = '?' + '&'.join(params) if params else ''

                

            except:
                form.add_error(None, "It wasn't possible to complete this search")
                query = ''
            else:
                path = reverse('browse_recipes') + query
                return HttpResponseRedirect(path)

        else:
            #recipe_list = Recipe.objects.all()
            #recipe_list = (1,2,3)
            path = reverse('browse_recipes') 
            return HttpResponseRedirect(path)

    else:  
        search_val = request.GET.get('search_val', '')
        tag_ids = request.GET.get('tags','')
        initial_data = {'search_field': search_val}
        if tag_ids:
            tag_ids = [int (tag_id) for tag_id in tag_ids.split(',')]
            initial_data['tags'] = tag_ids
        form = SearchRecipesForm(initial= initial_data)

        recipe_list = Recipe.objects.all()
        if search_val != '':
            #recipe_list = (6,7,8)
            recipe_list = recipe_list.filter(title__contains=search_val)

        if tag_ids:
            recipe_list = recipe_list.filter(tags__id__in=tag_ids).distinct()
        

    
    context = {'recipe_list' : recipe_list, 'form':form}
    
    return render(request, 'browse_recipes.html', context)
