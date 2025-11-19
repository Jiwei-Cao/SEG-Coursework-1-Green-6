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
    rated_recipes = sorted(
        recipes,
        key=lambda r: (r.average_rating, r.rating_count, -r.id),
        reverse=True
    )[:4]

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user, 'rated_recipes': rated_recipes})
