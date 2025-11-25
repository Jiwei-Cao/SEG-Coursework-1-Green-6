from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from ..models import Recipe, Rating, RecipeIngredient, RecipeMethod, Ingredient
from django.http import HttpResponseRedirect
from math import floor

@login_required
def get_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if is_rating_post(request):
        handle_rating_post(request, recipe)
        return HttpResponseRedirect(request.path_info)
    ingredients = getIngredientsList(recipe_id=recipe_id)
    method = getOrderedMethod(recipe_id=recipe_id)
    context = create_recipe_context(request.user, recipe, ingredients, method)
    return render(request, "specific_recipe.html", context)

def getIngredientsList(recipe_id):
    ingredients_dict_list = getIngredients(recipe_id=recipe_id)
    ingredients_list = []
    for ingredient_dict in ingredients_dict_list:
        quantity = ingredient_dict.get("quantity")
        unit = ingredient_dict.get("unit")
        ingredient = ingredient_dict.get("ingredient")
        ingredients_list.append("" + quantity + unit + " of " + ingredient)
    return ingredients_list

def getIngredients(recipe_id):
    recipe_ingredient_instances = RecipeIngredient.objects.filter(recipe__id = recipe_id)
    recipe_ingredients = []
    for recipe_ingredient in recipe_ingredient_instances:
        recipe_ingredient_dictionary = {
            "quantity": str(recipe_ingredient.quantity),
            "unit": str(recipe_ingredient.unit),
            "ingredient": str(recipe_ingredient.ingredient)
        }
        recipe_ingredients.append(recipe_ingredient_dictionary)
    return recipe_ingredients

def getOrderedMethod(recipe_id):
    recipe_steps = getMethod(recipe_id=recipe_id)
    current_step_num = 0
    ordered_method = []
    for recipe_step_dict in recipe_steps:
        order = recipe_step_dict.get("order")
        if order > current_step_num:
            instruction = recipe_step_dict.get("instruction")
            ordered_method.append(str(order) + ") " + instruction)
            current_step_num+=1
    return ordered_method


def getMethod(recipe_id):
    recipe_step_instances = RecipeMethod.objects.filter(recipe__id = recipe_id)
    recipe_steps = []
    for recipe_step in recipe_step_instances:
        recipe_step_dictionary = {
            "instruction": str(recipe_step.step),
            "order": recipe_step.order
        }
        recipe_steps.append(recipe_step_dictionary)
    return recipe_steps

def is_rating_post(request):
    return request.method == "POST" and request.POST.get("form_type") == "rating_form"

def handle_rating_post(request, recipe):
    rating_value = request.POST.get("rating")
    if not rating_value:
        return
    try:
        rating_value = int(rating_value)
    except ValueError:
        return
    if 1 <= rating_value <= 5:
        Rating.objects.update_or_create(
            user=request.user,
            recipe=recipe,
            defaults={'rating': rating_value}
        )

def get_user_rating(user,recipe):
    rating = Rating.objects.filter(user=user, recipe=recipe).first()
    return rating.rating if rating else None

def calculate_star_distribution(average_rating):
    full_stars = int(floor(average_rating))
    half_star = 1 if average_rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    return full_stars, half_star, empty_stars

def create_recipe_context(user,recipe, ingredients, method):
    ingredients = ingredients
    method = method
    user_rating = get_user_rating(user, recipe)
    average_rating = recipe.average_rating
    rating_count = recipe.rating_count
    full_stars, half_star, empty_stars = calculate_star_distribution(average_rating)

    return {
        "recipe": recipe,
        "ingredients": ingredients,
        "method": method,
        "user_rating": user_rating,
        "average_rating": average_rating, 
        "rating_count": rating_count,
        "full_stars": range(full_stars),
        "half_star": half_star,
        "empty_stars": range(empty_stars),
    }
