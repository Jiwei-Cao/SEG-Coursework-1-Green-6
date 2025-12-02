"""Integration tests for the Recipe model. This isn't strictly a unit test as it depends on data being in the database"""

import django
import json
import pytest

from recipes.models import Recipe, RecipeIngredient, Ingredient, User, Unit, MethodStep, Tag
from django.test import TestCase
from recipes.logic.classification import is_vegetarian, is_nut_free, is_gluten_free, is_vegan, is_dairy_free, \
    classify_recipe

#pytest creates a test database as specified in test.recipify.settings specifically for testing and then tears it down
@pytest.mark.django_db
class RecipeModelTestCase(TestCase):

    def setUp(self):
        def handle(self, *args, **options):
            """
            Django entrypoint for the command.

            Runs the full seeding workflow and stores ``self.users`` for any
            post-processing or debugging (not required for operation).
            """
        hbh_user = User.objects.create_user(username='@hbh_test', email='hbh@example.com', password='Recipify!',
                                        first_name='Haf', last_name='Bhudye', )

        end_user = User.objects.get(username='@hbh_test')

        """Construct default tags for the Tag Model"""
        tags = [
            {"name": "Vegan", "colour": "#2f88ff"},
            {"name": "Vegetarian", "colour": "#0d96b6"},
            {"name": "Gluten-free", "colour": "#d59d4d"},
            {"name": "Quick", "colour:":"#b26459"},
            {"name": "Easy", "colour": "#b26459"},
            {"name": "Mediterranean", "colour": "#e9dfec"},
            {"name": "Asian", "colour": "#b3a496"},
            {"name": "Indian", "colour": "#82ae67"},
            {"name": "Dairy-free", "colour": "#f67fcb"}
        ]
        for tag in tags:
            try:
                Tag.objects.create(name=tag["name"], colour=tag["colour"])
            except:
                pass


        # Units
        kilograms = Unit.objects.create(name='kilograms', symbol='kgs', user=end_user)
        kilograms.save()
        pounds = Unit.objects.create(name='pounds', symbol='lbs', user=end_user)
        pounds.save()
        teaspoons = Unit.objects.create(name='teaspoons', symbol='tsps', user=end_user)
        teaspoons.save()
        tablespoons = Unit.objects.create(name='tablespoons', symbol='tbsps', user=end_user)
        tablespoons.save()
        litres = Unit.objects.create(name='litres', symbol='ltrs', user=end_user)
        litres.save()
        units = Unit.objects.create(name='units', symbol='units', user=end_user)
        units.save()

        # Ingredients
        beef = Ingredient.objects.create(name='beef', category=Ingredient.BUTCHERY, user=end_user)
        beef.save()
        potato = Ingredient.objects.create(name='potato', category=Ingredient.VEGETABLE, user=end_user)
        potato.save()
        rice = Ingredient.objects.create(name='rice', category=Ingredient.GRAINS, user=end_user)
        rice.save()
        chicken = Ingredient.objects.create(name='chicken', category=Ingredient.BUTCHERY, user=end_user)
        chicken.save()
        lamb = Ingredient.objects.create(name='lamb', category=Ingredient.BUTCHERY, user=end_user)
        lamb.save()
        onions = Ingredient.objects.create(name='onions', category=Ingredient.ALLUM, user=end_user)
        onions.save()
        garlic = Ingredient.objects.create(name='garlic', category=Ingredient.ALLUM, user=end_user)
        garlic.save()
        salt = Ingredient.objects.create(name='salt', category=Ingredient.MINERALS, user=end_user)
        salt.save()
        pepper = Ingredient.objects.create(name='pepper', category=Ingredient.SPICE, user=end_user)
        pepper.save()
        pistachio = Ingredient.objects.create(name='pistachio', category=Ingredient.NUT, user=end_user)
        pistachio.save()
        lentil = Ingredient.objects.create(name='lentil', category=Ingredient.PULSES, user=end_user)
        lentil.save()
        water = Ingredient.objects.create(name='water', category=Ingredient.WATER, user=end_user)
        water.save()
        milk = Ingredient.objects.create(name='milk', category=Ingredient.DAIRY, user=end_user)
        milk.save()

        # Briani
        briani_step1 = MethodStep.objects.create(method_text="Cut the beef into cubes", step_number=1)
        briani_step2 = MethodStep.objects.create(method_text="Cut the potato into quarters", step_number=2)
        briani_step3 = MethodStep.objects.create(method_text="Soak the beef in the spice overnight", step_number=3)

        briani_recipe = Recipe.objects.create(title='Bryani', description='Bryani bef', user=end_user)
        briani_recipe.save()
        briani_recipe.method_steps.set([briani_step1, briani_step2, briani_step3])
        two_kgs_beef_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=beef,
                                                                 recipe=briani_recipe, user=end_user)
        two_kgs_potato_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=potato,
                                                                   recipe=briani_recipe, user=end_user)
        one_kgs_rice_in_briani = RecipeIngredient.objects.create(quantity=1, unit=kilograms, ingredient=rice,
                                                                 recipe=briani_recipe, user=end_user)
        two_kgs_onions_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=onions,
                                                                   recipe=briani_recipe, user=end_user)
        classify_recipe(briani_recipe)

        # Kaalia
        kaalia_step1 = MethodStep.objects.create(method_text="Cut the lamb into cubes", step_number=1)
        kaalia_step2 = MethodStep.objects.create(method_text="Cut the potato into quarters", step_number=2)
        kaalia_step3 = MethodStep.objects.create(method_text="Soak the lamb in water overnight", step_number=3)
        kaalia_recipe = Recipe.objects.create(title='Kalia', description='Kalia bef', user=end_user)
        kaalia_recipe.save()
        kaalia_recipe.method_steps.set([kaalia_step1, kaalia_step2, kaalia_step3])
        two_kgs_beef_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=beef,
                                                                 recipe=kaalia_recipe, user=end_user)
        two_kgs_potato_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=potato,
                                                                   recipe=kaalia_recipe, user=end_user)
        one_kgs_lamb_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=kilograms, ingredient=lamb,
                                                                 recipe=kaalia_recipe, user=end_user)
        two_kgs_onions_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=onions,
                                                                   recipe=kaalia_recipe, user=end_user)
        one_kgs_pistachio_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=kilograms,
                                                                      ingredient=pistachio, recipe=kaalia_recipe,
                                                                      user=end_user)
        one_litres_milk_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=litres, ingredient=milk,
                                                                    recipe=kaalia_recipe, user=end_user)
        classify_recipe(kaalia_recipe)

        # Lentil soup
        lentil_step1 = MethodStep.objects.create(method_text="Soak the lentils overnight", step_number=1)
        lentil_step2 = MethodStep.objects.create(method_text="Dice the onions", step_number=2)
        lentil_step3 = MethodStep.objects.create(method_text="Dice the garlic", step_number=3)
        lentil_recipe = Recipe.objects.create(title='Lentille', description='Soupe de lentille', user=end_user)
        lentil_recipe.save()
        lentil_recipe.method_steps.set([lentil_step1, lentil_step2, lentil_step3])
        one_kgs_lentil_in_lentil = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=lentil,
                                                                   recipe=lentil_recipe, user=end_user)
        one_litre_water_in_lentil = RecipeIngredient.objects.create(quantity=1, unit=litres, ingredient=water,
                                                                    recipe=lentil_recipe, user=end_user)
        two_units_onions_in_lentil = RecipeIngredient.objects.create(quantity=2, unit=units, ingredient=onions,
                                                                     recipe=lentil_recipe, user=end_user)
        one_units_garlic_in_lentil = RecipeIngredient.objects.create(quantity=1, unit=units, ingredient=garlic,
                                                                     recipe=lentil_recipe, user=end_user)
        classify_recipe(lentil_recipe)

        self.recipes = Recipe.objects.all()


    def test_create_recipe(self):

        recipe_dictionary = {}
        for recipe in self.recipes:
            recipe_id = recipe.id
            recipe_ingredient_instances = RecipeIngredient.objects.filter(recipe__id=recipe_id)
            recipe_ingredients = []
            for recipe_ingredient in recipe_ingredient_instances:
                recipe_ingredient_dictionary = {
                    "quantity": recipe_ingredient.quantity,
                    "unit": recipe_ingredient.unit,
                    "ingredient": recipe_ingredient.ingredient
                }
                recipe_ingredients.append(recipe_ingredient_dictionary)


            recipe_object = {
                "recipe_id": recipe_id,
                "recipe_title": recipe.title,
                "recipe_ingredients": recipe_ingredients,
            }
            recipe_dictionary[recipe.title] = recipe_object

        json_data = json.dumps(recipe_dictionary, indent=4, default=str)
        print(json_data)

        assert len(recipe_dictionary) == len(self.recipes)


    def test_briani_is_classified_correctly(self):
        braini_recipe = Recipe.objects.get(title='Bryani')
        assert not is_vegetarian(braini_recipe.pk)
        assert is_nut_free(braini_recipe.pk)
        assert is_gluten_free(braini_recipe.pk)
        assert not is_vegan(braini_recipe.pk)
        assert is_dairy_free(braini_recipe.pk)


    def test_kaalia_is_classified_correctly(self):
        kaalia_recipe = Recipe.objects.get(title='Kalia')
        assert not is_vegetarian(kaalia_recipe.pk)
        assert not is_nut_free(kaalia_recipe.pk)
        assert is_gluten_free(kaalia_recipe.pk)
        assert not is_vegan(kaalia_recipe.pk)
        assert not is_dairy_free(kaalia_recipe.pk)

    def test_lentil_soup_is_classified_correctly(self):
        lentil_recipe = Recipe.objects.get(title='Lentille')
        assert is_vegetarian(lentil_recipe.pk)
        assert is_nut_free(lentil_recipe.pk)
        assert is_gluten_free(lentil_recipe.pk)
        assert is_vegan(lentil_recipe.pk)
        assert is_dairy_free(lentil_recipe.pk)

