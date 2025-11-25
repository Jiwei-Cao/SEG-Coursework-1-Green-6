"""Integration tests for the Recipe model. This isn't strictly a unit test as it depends on data being in the database"""
from unittest import skipIf, skip

import django
import json
import pytest

django.setup()

from recipes.models import Recipe, RecipeIngredient, RecipeMethod
from django.test import TestCase

class RecipeModelTestCase(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.recipes = Recipe.objects.all()

    # @skip
    def test_create_recipe(self):

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

            recipe_dictionary = {
                "recipe_id": recipe_id,
                "recipe_title": recipe.title,
                "recipe_ingredients": recipe_ingredients,
                "recipe_steps": recipe_steps,
            }
            recipe_list.append(recipe_dictionary)


        json_data = json.dumps(recipe_list, indent=4, default=str)
        print(json_data)

        assert len(recipe_list) is not 0