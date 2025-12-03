from recipes.models import Recipe, RecipeIngredient, Ingredient, Tag


def classify_recipe(recipe):
    tags = [
        {"name": "Vegan", "colour": "#2f88ff"},
        {"name": "Vegetarian", "colour": "#0d96b6"},
        {"name": "Gluten-free", "colour": "#d59d4d"},
        {"name": "Quick", "colour:": "#b26459"},
        {"name": "Easy", "colour": "#b26459"},
        {"name": "Mediterranean", "colour": "#e9dfec"},
        {"name": "Asian", "colour": "#b3a496"},
        {"name": "Indian", "colour": "#82ae67"},
        {"name": "Dairy-free", "colour": "#f67fcb"}
    ]
    if is_vegetarian(recipe.id):
        vegetarian_tag = Tag.objects.get(name="Vegetarian")
        recipe.tags.add(vegetarian_tag)
    if is_vegan(recipe.id):
        vegan_tag = Tag.objects.get(name="Vegan")
        recipe.tags.add(vegan_tag)
    if is_gluten_free(recipe.id):
        gluten_free_tag = Tag.objects.get(name="Gluten-free")
        recipe.tags.add(gluten_free_tag)
    if is_dairy_free(recipe.id):
        dairy_free_tag = Tag.objects.get(name="Dairy-free")
        recipe.tags.add(dairy_free_tag)

def is_vegetarian(recipe_id):
    if do_recipe_ingredients_contain(recipe_id, [Ingredient.BUTCHERY, Ingredient.SEAFOOD]):
        return False
    return True

def is_vegan(recipe_id):
    if is_vegetarian(recipe_id):
        # A meal will qualify as vegan if it qualifies as vegetarian first
        if do_recipe_ingredients_contain(recipe_id, [Ingredient.EGG, Ingredient.DAIRY]):
            return False
        else:
            return True
    else:
        return False


def is_nut_free(recipe_id):
    if do_recipe_ingredients_contain(recipe_id, Ingredient.NUT):
        return False
    return True


def is_gluten_free(recipe_id):
    if do_recipe_ingredients_contain(recipe_id, Ingredient.GLUTEN):
        return False
    return True

def is_dairy_free(recipe_id):
    if do_recipe_ingredients_contain(recipe_id, Ingredient.DAIRY):
        return False
    return True

def do_recipe_ingredients_contain(recipe_id, ingredient_categories):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    for recipe_ingredient in recipe_ingredients:
        if recipe_ingredient.ingredient.category in ingredient_categories:
            return True

    return False

