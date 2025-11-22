from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Recipe, Rating

from math import floor

@login_required
def dashboard(request):
    """
    Display the current user's dashboard.

    This view renders the dashboard page for the authenticated user.
    It ensures that only logged-in users can access the page. If a user
    is not authenticated, they are automatically redirected to the login
    page.
    """
    
    recipes = Recipe.objects.filter(public=True)
    recipes = recipes.filter(rating__isnull=False).distinct()
    rated_recipes = sorted(
        recipes,
        key=lambda r: (r.average_rating, r.rating_count, -r.id),
        reverse=True
    )[:4]

    for recipe in rated_recipes:
        star_rating(recipe)

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user, 'rated_recipes': rated_recipes})

def star_rating(recipe):
    avg = recipe.average_rating or 0
    full_star = floor(avg)
    half_star = 1 if (avg - full_star) >= 0.5 else 0
    empty = 5 - full_star - half_star
    
    recipe.full_stars = range(full_star)
    recipe.half_stars = half_star
    recipe.empty_stars = range(empty)
