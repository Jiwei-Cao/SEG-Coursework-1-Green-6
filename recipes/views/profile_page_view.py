from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from math import floor

from recipes.models import Recipe, Rating, User


@login_required
def profile_page(request, username=None):
    """
    Displays either the current user's profile (if no username is provided)
    or another user's profile (if username is provided)
    """

    if username is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, username=username)

    recipes = Recipe.objects.filter(user=profile_user)

    rating_count = calculate_user_rating(profile_user,recipes)

    full_stars,half_star, empty_stars = star_rating(profile_user.rating)

    following_count = profile_user.following.count()
    follower_count = profile_user.followers.count()

    is_following = False

    if profile_user != request.user:
        is_following = profile_user.id in request.user.following.values_list('id', flat=True)

    return render(request, 'profile_page.html', {
        'user': profile_user,
        'recipes':recipes,
        'rating_count': rating_count,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        'following_count': following_count,
        'follower_count': follower_count,
        'is_following': is_following,
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