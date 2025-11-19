from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Recipe, Rating


@login_required
def dashboard(request):
    """
    Display the current user's dashboard.

    This view renders the dashboard page for the authenticated user.
    It ensures that only logged-in users can access the page. If a user
    is not authenticated, they are automatically redirected to the login
    page.
    """

    recipes = Recipe.objects.all()
    rated_recipes = []
    if recipes.exists():
        for recipe in recipes:
            all_ratings = Rating.objects.filter(recipe=recipe)
            average_rating = None
            if all_ratings.exists():
                average_rating = sum(r.rating for r in all_ratings) / all_ratings.count()
                recipe.average_rating = average_rating
                recipe.rating_count = all_ratings.count()
                print("Average rating: " + str(recipe.average_rating))
            else:
                recipe.average_rating = 0
                recipe.rating_count = 0
        rated_recipes = sorted(recipes, key=lambda r: (r.average_rating,r.rating_count), reverse=True)[:4]

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user, 'rated_recipes': rated_recipes})
