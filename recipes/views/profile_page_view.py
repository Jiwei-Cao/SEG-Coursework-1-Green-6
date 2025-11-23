from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from math import floor

from recipes.models import Recipe
from recipes.models import Rating


@login_required
def profile_page(request):
    """
    Display's the current user's profile.
    """
    
    current_user = request.user

    recipes = Recipe.objects.filter(user=current_user)

    rating_count = calculate_user_rating(current_user,recipes)

    full_stars,half_star, empty_stars = star_rating(current_user.rating)

    return render(request, 'profile_page.html', {
        'user': current_user,
        'recipes':recipes,
        'rating_count': rating_count,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        })

def calculate_user_rating(user,recipes):
    all_ratings = Rating.objects.filter(recipe__in=recipes)
    rating_count = all_ratings.count()
    ratings_sum = sum(rating.rating for rating in all_ratings)
    total_ratings = all_ratings.count()
    user_rating = ratings_sum / total_ratings if total_ratings > 0 else 0
    user.rating = user_rating
    return rating_count

def star_rating(rating):
    rating = round(rating * 2) / 2
    full_stars = int(floor(rating))
    half_star = rating-full_stars==0.5
    empty_stars = 5 - full_stars - half_star
    return (full_stars, half_star, empty_stars)