from recipes.models import RecipeIngredient, Recipe

def test_create_recipe(self):
    self.recipes = Recipe.objects.all()
    # This holds the list of complete recipes
    recipe_list = []
    for recipe in self.recipes:
        recipe_id = recipe.id
        print(recipe_id)

        recipe_ingredient_instances = RecipeIngredient.objects.filter(recipe__id = recipe_id)
        recipe_ingredients = []
        for recipe_ingredient in recipe_ingredient_instances:
            recipe_ingredient_dictionary = {
                "quantity": recipe_ingredient.quantity,
                "unit": recipe_ingredient.unit,
                "ingredient": recipe_ingredient.ingredient
            }
            recipe_ingredients.append(recipe_ingredient_dictionary)

        recipe_step_instances = RecipeMethod.objects.filter(recipe__id = recipe_id)
        recipe_steps = []
        for recipe_step in recipe_step_instances:
            recipe_step_dictionary = {
                "instruction": recipe_step.step,
                "order": recipe_step.order
            }
            recipe_steps.append(recipe_step_dictionary)

        # Build the complete recipe object with summary recipe information, list of ingredients and list of steps
        recipe_dictionary = {
            "recipe_id": recipe_id,
            "recipe_title": recipe.title,
            "recipe_ingredients": recipe_ingredients,
            "recipe_steps": recipe_steps,
        }

        recipe_list.append(recipe_dictionary)