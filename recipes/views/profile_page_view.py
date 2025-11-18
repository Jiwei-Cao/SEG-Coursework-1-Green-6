from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from math import floor

from recipes.models import Favourite
from recipes.models import Recipe
from recipes.models import Recipe

@login_required
def profile_page(request):
    """
    Display's the current user's profile.
    """
    
    current_user = request.user

    recipes = Recipe.objects.filter(user=current_user)

    rating = round(current_user.rating * 2) / 2
    full_stars = int(floor(rating))
    half_star = rating-full_stars==0.5
    empty_stars = 5 - full_stars - half_star


    favourite_recipes = []
    favourite_recipe_ids = Favourite.objects.filter(user=current_user).values_list('recipe', flat=True)
    for item in Recipe.objects.all():
        if item.pk in favourite_recipe_ids:
            favourite_recipes.append(item)



    return render(request, 'profile_page.html', {
        'user': current_user,
        'recipes':recipes,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        'favourite_recipes':  favourite_recipes
        })