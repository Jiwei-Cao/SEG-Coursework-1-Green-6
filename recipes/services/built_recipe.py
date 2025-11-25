from recipes.models import RecipeIngredient, RecipeMethod, Recipe

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
            "quantity": recipe_ingredient.quantity,
            "unit": recipe_ingredient.unit,
            "ingredient": recipe_ingredient.ingredient
        }
        recipe_ingredients.append(recipe_ingredient_dictionary)
    return recipe_ingredients

def getOrderedMethod(recipe_id):
    recipe_steps = getMethod(recipe_id=recipe_id)
    current_step_num = 0
    ordered_method = []
    for recipe_step_dict in recipe_steps:
        order = recipe_step_dict.get("order")
        if order == current_step_num+1:
            instruction = recipe_step_dict.get("instruction")
            ordered_method.append(str(order) + ") " + instruction)
            current_step_num+=1
    return ordered_method

def getMethod(recipe_id):
    recipe_step_instances = RecipeMethod.objects.filter(recipe__id = recipe_id)
    recipe_steps = []
    for recipe_step in recipe_step_instances:
        recipe_step_dictionary = {
            "instruction": recipe_step.step,
            "order": recipe_step.order
        }
        recipe_steps.append(recipe_step_dictionary)
    return recipe_steps

def returnWholeRecipe(recipe_id):
    recipe = Recipe.objects.get(recipe_id)
    recipe_ingredients = getIngredients(recipe_id)
    recipe_steps = getMethod(recipe_id)
    recipe_dictionary = {
    "recipe_id": recipe_id,
    "recipe": recipe,
    "recipe_title": recipe.title,
    "recipe_ingredients": recipe_ingredients,
    "recipe_steps": recipe_steps,
    }
    return recipe_dictionary