"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to ``USER_COUNT`` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""
import argparse

from recipes.logic.classification import classify_recipe
from recipes.models import Recipe, RecipeIngredient, Ingredient, Unit, MethodStep
from django.core.management.base import BaseCommand
from recipes.models import User


class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (``user_fixtures``) and then
    repeatedly generates additional random users until ``USER_COUNT`` total users
    exist in the database. Each generated user receives the same default password.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('flag', type=str, nargs='?', default='retain')


    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.users`` for any
        post-processing or debugging (not required for operation).
        """
        empty_flag = options.get('flag', None)
        print(empty_flag)

        if empty_flag == 'afresh':

            print('Starting afresh by deleting existing data')
            # Reset database except users
            Unit.objects.all().delete()
            Ingredient.objects.all().delete()
            Recipe.objects.all().delete()
            RecipeIngredient.objects.all().delete()
            MethodStep.objects.all().delete()

        end_user = User.objects.get(username='@johndoe')

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

        briani_recipe = Recipe.objects.create(title='briani', description='briani', user=end_user)
        briani_recipe.save()
        briani_recipe.method_steps.set([briani_step1, briani_step2, briani_step3])
        two_kgs_beef_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=beef, recipe=briani_recipe, user=end_user)
        two_kgs_potato_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=potato, recipe=briani_recipe, user=end_user)
        one_kgs_rice_in_briani = RecipeIngredient.objects.create(quantity=1, unit=kilograms, ingredient=rice, recipe=briani_recipe, user=end_user)
        two_kgs_onions_in_briani = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=onions, recipe=briani_recipe, user=end_user)
        classify_recipe(briani_recipe)


        # Kaalia
        kaalia_step1 = MethodStep.objects.create(method_text="Cut the lamb into cubes", step_number=1)
        kaalia_step2 = MethodStep.objects.create(method_text="Cut the potato into quarters", step_number=2)
        kaalia_step3 = MethodStep.objects.create(method_text="Soak the lamb in water overnight", step_number=3)
        kaalia_recipe = Recipe.objects.create(title='kaalia', description='kaalia', user=end_user)
        kaalia_recipe.save()
        kaalia_recipe.method_steps.set([kaalia_step1, kaalia_step2, kaalia_step3])
        two_kgs_beef_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=beef, recipe=kaalia_recipe, user=end_user)
        two_kgs_potato_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=potato, recipe=kaalia_recipe, user=end_user)
        one_kgs_lamb_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=kilograms, ingredient=lamb, recipe=kaalia_recipe, user=end_user)
        two_kgs_onions_in_kaalia = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=onions, recipe=kaalia_recipe, user=end_user)
        one_kgs_pistachio_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=kilograms, ingredient=pistachio, recipe=kaalia_recipe, user=end_user)
        one_litres_milk_in_kaalia = RecipeIngredient.objects.create(quantity=1, unit=litres, ingredient=milk, recipe=kaalia_recipe, user=end_user)
        classify_recipe(kaalia_recipe)

        # Lentil soup
        lentil_step1 = MethodStep.objects.create(method_text="Soak the lentils overnight", step_number=1)
        lentil_step2 = MethodStep.objects.create(method_text="Dice the onions", step_number=2)
        lentil_step3 = MethodStep.objects.create(method_text="Dice the garlic", step_number=3)
        lentil_recipe = Recipe.objects.create(title='lentil', description='lentil', user=end_user)
        lentil_recipe.save()
        lentil_recipe.method_steps.set([lentil_step1, lentil_step2, lentil_step3])
        one_kgs_lentil_in_lentil = RecipeIngredient.objects.create(quantity=2, unit=kilograms, ingredient=lentil, recipe=lentil_recipe, user=end_user)
        one_litre_water_in_lentil = RecipeIngredient.objects.create(quantity=1, unit=litres, ingredient=water, recipe=lentil_recipe, user=end_user)
        two_units_onions_in_lentil = RecipeIngredient.objects.create(quantity=2, unit=units, ingredient=onions, recipe=lentil_recipe, user=end_user)
        one_units_garlic_in_lentil = RecipeIngredient.objects.create(quantity=1, unit=units, ingredient=garlic, recipe=lentil_recipe, user=end_user)
        classify_recipe(lentil_recipe)


