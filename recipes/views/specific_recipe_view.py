from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
from django.db.models import F
from ..models import Recipe, Rating, RecipeIngredient, UserIngredient
from django.http import HttpResponseRedirect
from math import floor

from ..models import Recipe, Rating
from ..forms import CommentForm 

@login_required
def get_recipe(request, recipe_id):
    """Gets the information for recipe that user has clicked"""

    recipe = get_object_or_404(Recipe, id=recipe_id)

    multiplier = int(request.GET.get('multiplier',1))

    if request.method == "POST" and request.POST.get("form_type")=="rating_form":
        handle_rating_post(request, recipe)
        return HttpResponseRedirect(request.path_info)


    ingredients = getIngredients(recipe_id=recipe_id, multiplier=multiplier)
    context = create_recipe_context(request.user, recipe, ingredients, multiplier, CommentForm())
    return render(request, "specific_recipe.html", context)

def getIngredients(recipe_id, multiplier):
    """Get ingredients for specified recipe, including the amount required, units, and ingredient name"""

    recipe_ingredient_instances = RecipeIngredient.objects.filter(recipe__id = recipe_id)
    recipe_ingredients = recipe_ingredient_instances.annotate(scaled_quantity=F('quantity')*multiplier)
    return recipe_ingredients

def handle_rating_post(request, recipe):
    """Checks if rating is valid, if so creates new rating entry for specified recipe"""

    rating_value = request.POST.get("rating")
    if not rating_value:
        return
    try:
        rating_value = int(rating_value)
    except ValueError:
        return
    if not 1 <= rating_value <= 5:
        return
    Rating.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={'rating': rating_value}
    )

def get_user_rating(user, recipe):
    rating = Rating.objects.filter(user=user, recipe=recipe).first()
    return rating.rating if rating else None

def calculate_star_distribution(average_rating):
    """Calculates the number of full, half and empty stars for specified recipe according to average rating (rounded to nearest 0.5)"""

    full_stars = int(floor(average_rating))
    half_star = 1 if average_rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return full_stars, half_star, empty_stars

def create_recipe_context(user, recipe, ingredients, multiplier, form):
    """Creates the context for specified recipe"""

    user_rating = get_user_rating(user, recipe)
    average_rating = recipe.average_rating or 0
    rating_count = recipe.rating_count or 0
    full_stars, half_star, empty_stars = calculate_star_distribution(average_rating)
    shopping_list = create_shopping_list(user, ingredients)
    recipe_comments_count = count_recipe_comments(recipe)

    return {
        "recipe": recipe,
        "ingredients": ingredients,
        "user_rating": user_rating,
        "average_rating": average_rating,
        "rating_count": rating_count,
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
        "multiplier": multiplier,
        "recipe_comments_count": recipe_comments_count,
        "form": form,
        "shopping_list": shopping_list,
     }

def count_recipe_comments(recipe):
    counter = 0
    parent_comments = recipe.comments.all()
    for parent_comment in parent_comments:
        counter = counter + parent_comment.replies.count()

    counter = counter + recipe.comments.count()
    return counter

def create_shopping_list(user, ingredients):
    cupboard = UserIngredient.objects.filter(user = user)
    cupboard_names = {ingredient.name for ingredient in cupboard}
    unit_to_grams = {'gs': 1, 'lbs': 453.592, 'kgs':1000}
    unit_to_mls = {'tsps': 5, 'tbsps': 15, 'mls': 1, 'ltrs': 1000}

    shopping_list = []
    for ingredient in ingredients:
        if ingredient.ingredient.name not in cupboard_names:
            ingredient.difference_quantity = ingredient.scaled_quantity
            shopping_list.append(ingredient)
            continue

        cupboard_ingredient = cupboard.get(name=ingredient.ingredient.name)
        try:
            if ingredient.unit.symbol in unit_to_grams:
                ingredient_qty = ingredient.scaled_quantity * unit_to_grams[ingredient.unit.symbol]
                cupboard_qty = cupboard_ingredient.quantity * unit_to_grams[cupboard_ingredient.unit.symbol]
            
            elif ingredient.unit.symbol in unit_to_mls:
                ingredient_qty = ingredient.scaled_quantity * unit_to_mls[ingredient.unit.symbol]
                cupboard_qty = cupboard_ingredient.quantity * unit_to_mls[cupboard_ingredient.unit.symbol]

            else:
                ingredient_qty = ingredient.scaled_quantity
                cupboard_qty = cupboard_ingredient.quantity

        except:
            ingredient.difference_quantity = ingredient.scaled_quantity
            shopping_list.append(ingredient)
            continue

        if ingredient_qty > cupboard_qty:
            difference_qty = ingredient_qty - cupboard_qty
            if ingredient.unit.symbol in unit_to_grams:
                ingredient.difference_quantity = difference_qty / unit_to_grams[ingredient.unit.symbol]
            elif ingredient.unit.symbol in unit_to_mls:
                ingredient.difference_quantity = difference_qty / unit_to_mls[ingredient.unit.symbol]
            else:
                ingredient.difference_quantity = difference_qty
            shopping_list.append(ingredient)
    return shopping_list
