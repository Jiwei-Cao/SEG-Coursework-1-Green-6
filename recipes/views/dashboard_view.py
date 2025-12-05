from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from ..models import Recipe, Rating

from math import floor

@login_required
def dashboard(request):
    current_user = request.user
    """
    Display the current user's dashboard.

    This view renders the dashboard page for the authenticated user.
    It ensures that only logged-in users can access the page. If a user
    is not authenticated, they are automatically redirected to the login
    page.
    """
    
    rated_recipes = get_top_rated_recipes(current_user)
    features = get_features()

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user, 'rated_recipes': rated_recipes, 'features':features})

def star_rating(recipe):
    avg = recipe.average_rating or 0
    full_star = floor(avg)
    half_star = 1 if (avg - full_star) >= 0.5 else 0
    empty = 5 - full_star - half_star
    
    recipe.full_stars = range(full_star)
    recipe.half_stars = half_star
    recipe.empty_stars = range(empty)

def get_top_rated_recipes(current_user):
    following_user = current_user.following.all()
    recipes = Recipe.objects.filter( Q(public=True) | Q(user__in=following_user) | Q(user=current_user)).distinct()

    recipes = recipes.filter(rating__isnull=False).distinct()
    rated_recipes = sorted(
        recipes,
        key=lambda r: (r.average_rating, r.rating_count, -r.id),
        reverse=True
    )[:4]

    for recipe in rated_recipes:
        star_rating(recipe)
    return rated_recipes

def get_features():
    return [
        {
            "title": "All Recipes",
            "icon": "bi-bookmark-plus",
            "description": "Find the perfect recipe based on your preferences, e.g. ingredients available, cooking time",
            "link": "all_recipes",
        },
        {
            "title": "Find other users",
            "icon": "bi-person-add",
            "description": "Find other passionate recipe creators and follow them to acccess follower-exclusive recipes",
            "link": "user_search",
        },
        {
            "title": "Create Your Recipe",
            "icon": "bi-file-earmark-text",
            "description": "Create and store your own recipe",
            "link": "create_recipe",
        },
        {
            "title": "Your Profile",
            "icon": "bi-person-circle",
            "description": "Have a look at what recipes you have created!!",
            "link": "profile_page",
        },
        {
            "title": "Cupboard",
            "icon": "bi-bookmark-plus",
            "description": "Tell us what ingredients you have",
            "link": "cupboard",
        },
    ]