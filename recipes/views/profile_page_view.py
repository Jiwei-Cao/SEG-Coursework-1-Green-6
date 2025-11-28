from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from math import floor
from django.db.models import Count


from recipes.models import Recipe, Rating, User


@login_required
def profile_page(request, username=None):
    """
    Displays either the current user's profile (if no username is provided)
    or another user's profile (if username is provided)
    """
    current_user = request.user

    if username is None:
        profile_user = request.user
    else:
        profile_user = get_object_or_404(User, username=username)

    recipes = Recipe.objects.filter(user=profile_user)

    rating_count = calculate_user_rating(profile_user,recipes)

    full_stars,half_star, empty_stars = star_rating(profile_user.rating)

    is_following = following(current_user,profile_user)

    favourite_recipe_ids = get_favourite_recipes_id(current_user)
    favourite_recipes = Recipe.objects.filter(pk__in=favourite_recipe_ids)

    most_popular_recipe = recipes.order_by('-rating').first()
    most_popular_id = most_popular_recipe.id if most_popular_recipe else None

    most_favourited_recipe = (
        recipes
        .annotate(fav_count=Count('favourites'))
        .order_by('-fav_count', '-created_at')
        .first()                          
    )
    most_favourited_recipe_id = most_favourited_recipe.id if most_favourited_recipe else None

    if request.method == 'POST':
        handle_favourites_form_requests(request)

        return HttpResponseRedirect(request.path_info)

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
        'favourite_recipes':  favourite_recipes,
        'user_favourited_recipe_ids': favourite_recipe_ids,
        'most_popular': most_popular_id,
        'most_favourite': most_favourited_recipe_id
        })

@login_required
def following_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = profile_user.following.all()

    following_ids= set(request.user.following.values_list('id', flat=True))

    return render(request, 'user_list.html', {
        'title': f"{profile_user.username} is following",
        'profile_user': profile_user,
        'users': following,
        'following_ids': following_ids,
    })

@login_required 
def followers_list(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = profile_user.followers.all()

    following_ids = set(request.user.following.values_list('id', flat=True))

    return render(request, 'user_list.html', {
        'title': f"{profile_user.username}'s followers",
        'profile_user': profile_user,
        'users': followers,
        'following_ids': following_ids,
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

def get_favourite_recipes_id(user):
    return list(
        user.recipes_favourited.values_list('id', flat=True)
    )


def handle_favourites_form_requests(request):    
    if request.POST.get('favourite_recipe', '') == 'unfavourite_recipe':
        unfavourite_recipe(request)

def unfavourite_recipe(request):
    recipe_id = request.POST.get("recipe_clicked")

    if not recipe_id:
        return

    # Remove relationship
    request.user.recipes_favourited.remove(recipe_id)

def following(current_user, profile_user):
    return  current_user != profile_user and current_user.following.filter(id=profile_user.id).exists()
