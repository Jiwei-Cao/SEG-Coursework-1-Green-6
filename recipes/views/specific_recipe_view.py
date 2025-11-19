from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Recipe, Rating
from django.http import HttpResponse, Http404, HttpResponseRedirect
from math import floor
@login_required
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == "POST" and request.POST.get("form_type") == "rating_form":
        rating_value = request.POST.get("rating")
        if rating_value:
            try:
                rating_value = int(rating_value)
                if 1 <= rating_value <= 5:
                    Rating.objects.update_or_create(
                        user=request.user,
                        recipe=recipe,
                        defaults={'rating': rating_value}
                    )
            except ValueError:
                   pass
        return HttpResponseRedirect(request.path_info)
    
    try:
        user_rating = Rating.objects.get(user=request.user, recipe=recipe).rating
    except Rating.DoesNotExist:
        user_rating = None

    all_ratings = Rating.objects.filter(recipe=recipe)
    average_rating = recipe.average_rating
    rating_count = recipe.rating_count

    full_stars = int(floor(average_rating))
    half_star = 1 if average_rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star


    context = {
        "recipe": recipe,
        "user_rating": user_rating,
        "average_rating": average_rating, 
        "rating_count": rating_count,
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
    }
    return render(request, "specific_recipe.html", context)