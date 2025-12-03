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
        kilograms = Unit.objects.get_or_create(name='kilograms', symbol='kgs', user=end_user)[0]
        kilograms.save()
        pounds = Unit.objects.get_or_create(name='pounds', symbol='lbs', user=end_user)[0]
        pounds.save()
        teaspoons = Unit.objects.get_or_create(name='teaspoons', symbol='tsps', user=end_user)[0]
        teaspoons.save()
        tablespoons = Unit.objects.get_or_create(name='tablespoons', symbol='tbsps', user=end_user)[0]
        tablespoons.save()
        litres = Unit.objects.get_or_create(name='litres', symbol='ltrs', user=end_user)[0]
        litres.save()
        grams = Unit.objects.get_or_create(name='grams', symbol='kgs', user=end_user)[0]
        grams.save()
        units = Unit.objects.get_or_create(name='units', symbol='units', user=end_user)[0]
        units.save()

        # Ingredients
        beef = Ingredient.objects.get_or_create(name='beef', category=Ingredient.BUTCHERY, user=end_user)[0]
        beef.save()
        potato = Ingredient.objects.get_or_create(name='potato', category=Ingredient.VEGETABLE, user=end_user)[0]
        potato.save()
        rice = Ingredient.objects.get_or_create(name='rice', category=Ingredient.GRAINS, user=end_user)[0]
        rice.save()
        chicken = Ingredient.objects.get_or_create(name='chicken', category=Ingredient.BUTCHERY, user=end_user)[0]
        chicken.save()
        pork = Ingredient.objects.get_or_create(name='pork', category=Ingredient.BUTCHERY, user=end_user)[0]
        pork.save()
        lamb = Ingredient.objects.get_or_create(name='lamb', category=Ingredient.BUTCHERY, user=end_user)[0]
        lamb.save()
        onions = Ingredient.objects.get_or_create(name='onions', category=Ingredient.ALLUM, user=end_user)[0]
        onions.save()
        garlic = Ingredient.objects.get_or_create(name='garlic', category=Ingredient.ALLUM, user=end_user)[0]
        garlic.save()
        flour = Ingredient.objects.get_or_create(name='flour',category=Ingredient.MINERALS, user=end_user)[0]
        flour.save()
        salt = Ingredient.objects.get_or_create(name='salt', category=Ingredient.MINERALS, user=end_user)[0]
        salt.save()
        sugar = Ingredient.objects.get_or_create(name='sugar', category=Ingredient.MINERALS, user=end_user)[0]
        sugar.save()
        pepper = Ingredient.objects.get_or_create(name='pepper', category=Ingredient.SPICE, user=end_user)[0]
        pepper.save()
        cinnamon = Ingredient.objects.get_or_create(name='cinnamon', category=Ingredient.SPICE, user=end_user)[0]
        cinnamon.save()
        pistachio = Ingredient.objects.get_or_create(name='pistachio', category=Ingredient.NUT, user=end_user)[0]
        pistachio.save()
        almond = Ingredient.objects.get_or_create(name='almond', category=Ingredient.NUT, user=end_user)[0]
        almond.save()
        lentil = Ingredient.objects.get_or_create(name='lentil', category=Ingredient.PULSES, user=end_user)[0]
        lentil.save()
        water = Ingredient.objects.get_or_create(name='water', category=Ingredient.WATER, user=end_user)[0]
        water.save()
        milk = Ingredient.objects.get_or_create(name='milk', category=Ingredient.DAIRY, user=end_user)[0]
        milk.save()
        tomato = Ingredient.objects.get_or_create(name='tomato', category=Ingredient.VEGETABLE, user=end_user)[0]
        tomato.save()
        carrot = Ingredient.objects.get_or_create(name='carrot', category=Ingredient.VEGETABLE, user=end_user)[0]
        carrot.save()
        celery = Ingredient.objects.get_or_create(name='celery', category=Ingredient.VEGETABLE, user=end_user)[0] 
        celery.save()
        bell_pepper = Ingredient.objects.get_or_create(name='bell pepper', category=Ingredient.VEGETABLE, user=end_user)[0] 
        bell_pepper.save()
        mushroom = Ingredient.objects.get_or_create(name='mushroom', category=Ingredient.VEGETABLE, user=end_user)[0]
        mushroom.save()
        spinach = Ingredient.objects.get_or_create(name='spinach', category=Ingredient.VEGETABLE, user=end_user)[0] 
        spinach.save()
        courgette = Ingredient.objects.get_or_create(name='courgette', category=Ingredient.VEGETABLE, user=end_user)[0] 
        courgette.save()
        aubergine = Ingredient.objects.get_or_create(name='aubergine', category=Ingredient.VEGETABLE, user=end_user)[0] 
        aubergine.save()
        shallot = Ingredient.objects.get_or_create(name='shallot', category=Ingredient.ALLUM, user=end_user)[0]
        shallot.save()
        leek = Ingredient.objects.get_or_create(name='leek', category=Ingredient.ALLUM, user=end_user)[0] 
        leek.save()
        basil = Ingredient.objects.get_or_create(name='basil', category=Ingredient.HERBS, user=end_user)[0] 
        basil.save()
        parsley = Ingredient.objects.get_or_create(name='parsley', category=Ingredient.HERBS, user=end_user)[0]
        parsley.save()
        coriander = Ingredient.objects.get_or_create(name='coriander', category=Ingredient.HERBS, user=end_user)[0]
        coriander.save()
        thyme = Ingredient.objects.get_or_create(name='thyme', category=Ingredient.HERBS, user=end_user)[0]
        thyme.save()
        rosemary = Ingredient.objects.get_or_create(name='rosemary', category=Ingredient.HERBS, user=end_user)[0]
        rosemary.save()
        dill = Ingredient.objects.get_or_create(name='dill', category=Ingredient.HERBS, user=end_user)[0] 
        dill.save()
        cumin = Ingredient.objects.get_or_create(name='cumin', category=Ingredient.SPICE, user=end_user)[0] 
        cumin.save()
        turmeric = Ingredient.objects.get_or_create(name='turmeric', category=Ingredient.SPICE, user=end_user)[0] 
        turmeric.save()
        paprika = Ingredient.objects.get_or_create(name='paprika', category=Ingredient.SPICE, user=end_user)[0] 
        paprika.save()
        chili_powder = Ingredient.objects.get_or_create(name='chili powder', category=Ingredient.SPICE, user=end_user)[0] 
        chili_powder.save()
        nutmeg = Ingredient.objects.get_or_create(name='nutmeg', category=Ingredient.SPICE, user=end_user)[0] 
        nutmeg.save()
        cardamom = Ingredient.objects.get_or_create(name='cardamom', category=Ingredient.SPICE, user=end_user)[0] 
        cardamom.save()
        salmon = Ingredient.objects.get_or_create(name='salmon', category=Ingredient.SEAFOOD, user=end_user)[0] 
        salmon.save()
        shrimp = Ingredient.objects.get_or_create(name='shrimp', category=Ingredient.SEAFOOD, user=end_user)[0] 
        shrimp.save()
        tuna = Ingredient.objects.get_or_create(name='tuna', category=Ingredient.SEAFOOD, user=end_user)[0] 
        tuna.save()
        egg = Ingredient.objects.get_or_create(name='egg', category=Ingredient.EGG, user=end_user)[0] 
        egg.save()
        butter = Ingredient.objects.get_or_create(name='butter', category=Ingredient.DAIRY, user=end_user)[0] 
        butter.save()
        cream = Ingredient.objects.get_or_create(name='cream', category=Ingredient.DAIRY, user=end_user)[0] 
        cream.save()
        yogurt = Ingredient.objects.get_or_create(name='yogurt', category=Ingredient.DAIRY, user=end_user)[0] 
        yogurt.save()
        cheese = Ingredient.objects.get_or_create(name='cheese', category=Ingredient.DAIRY, user=end_user)[0] 
        cheese.save()
        pasta = Ingredient.objects.get_or_create(name='pasta', category=Ingredient.GLUTEN, user=end_user)[0] 
        pasta.save()
        bread = Ingredient.objects.get_or_create(name='bread', category=Ingredient.GLUTEN, user=end_user)[0] 
        bread.save()
        quinoa = Ingredient.objects.get_or_create(name='quinoa', category=Ingredient.GRAINS, user=end_user)[0] 
        quinoa.save()
        chickpeas = Ingredient.objects.get_or_create(name='chickpeas', category=Ingredient.PULSES, user=end_user)[0] 
        chickpeas.save()
        beans = Ingredient.objects.get_or_create(name='beans', category=Ingredient.PULSES, user=end_user)[0] 
        beans.save()
        baking_powder = Ingredient.objects.get_or_create(name='baking powder', category=Ingredient.MINERALS, user=end_user)[0] 
        baking_powder.save()
        baking_soda = Ingredient.objects.get_or_create(name='baking soda', category=Ingredient.MINERALS, user=end_user)[0] 
        baking_soda.save()
        strawberry = Ingredient.objects.get_or_create(name='strawberry', category=Ingredient.FRUIT, user=end_user)[0] 
        
        strawberry.save()
        banana = Ingredient.objects.get_or_create(name='banana', category=Ingredient.FRUIT, user=end_user)[0] 
        banana.save()
        lemon = Ingredient.objects.get_or_create(name='lemon', category=Ingredient.FRUIT, user=end_user)[0] 
        lemon.save()
        orange = Ingredient.objects.get_or_create(name='orange', category=Ingredient.FRUIT, user=end_user)[0] 
        orange.save()
        apple = Ingredient.objects.get_or_create(name='apple', category=Ingredient.FRUIT, user=end_user)[0] 
        apple.save()
        blueberry = Ingredient.objects.get_or_create(name='blueberry', category=Ingredient.FRUIT, user=end_user)[0] 
        blueberry.save()
        honey = Ingredient.objects.get_or_create(name='honey', category=Ingredient.MINERALS, user=end_user)[0] 
        honey.save()
        maple_syrup = Ingredient.objects.get_or_create(name='maple syrup', category=Ingredient.MINERALS, user=end_user)[0] 
        maple_syrup.save()
        chocolate = Ingredient.objects.get_or_create(name='chocolate', category=Ingredient.MINERALS, user=end_user)[0] 
        chocolate.save()
        cocoa_powder = Ingredient.objects.get_or_create(name='cocoa powder', category=Ingredient.SPICE, user=end_user)[0] 
        cocoa_powder.save()
        vanilla = Ingredient.objects.get_or_create(name='vanilla', category=Ingredient.SPICE, user=end_user)[0] 
        vanilla.save()

        # Briani recipe
        briani_recipe, _ = Recipe.objects.update_or_create(
            title='briani',
            defaults={'description': 'briani', 'user': end_user}
        )

        # Create or update steps
        briani_step1, _ = MethodStep.objects.update_or_create(
            step_number=1,
            method_text="Cut the beef into cubes"
        )
        briani_step2, _ = MethodStep.objects.update_or_create(
            step_number=2,
            method_text="Cut the potato into quarters"
        )
        briani_step3, _ = MethodStep.objects.update_or_create(
            step_number=3,
            method_text="Soak the beef in the spice overnight"
        )

        # Assign steps to the recipe
        briani_recipe.method_steps.set([briani_step1, briani_step2, briani_step3])


        two_kgs_beef_in_briani = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=beef, recipe=briani_recipe, user=end_user)
        two_kgs_potato_in_briani = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=potato, recipe=briani_recipe, user=end_user)
        one_kgs_rice_in_briani = RecipeIngredient.objects.get_or_create(quantity=1, unit=kilograms, ingredient=rice, recipe=briani_recipe, user=end_user)
        two_kgs_onions_in_briani = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=onions, recipe=briani_recipe, user=end_user)
        classify_recipe(briani_recipe)


        # Create or update Kaalia recipe
        kaalia_recipe, _ = Recipe.objects.update_or_create(
            title='kaalia',
            defaults={'description': 'kaalia', 'user': end_user}
        )

        # Create or update MethodStep objects (global)
        kaalia_step1, _ = MethodStep.objects.update_or_create(
            step_number=1,
            method_text="Cut the lamb into cubes"
        )

        kaalia_step2, _ = MethodStep.objects.update_or_create(
            step_number=2,
            method_text="Cut the potato into quarters"
        )

        kaalia_step3, _ = MethodStep.objects.update_or_create(
            step_number=3,
            method_text="Soak the lamb in water overnight"
        )

        # Link steps to the recipe via ManyToMany
        kaalia_recipe.method_steps.set([kaalia_step1, kaalia_step2, kaalia_step3])


        two_kgs_beef_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=beef, recipe=kaalia_recipe, user=end_user)
        two_kgs_potato_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=potato, recipe=kaalia_recipe, user=end_user)
        one_kgs_lamb_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=1, unit=kilograms, ingredient=lamb, recipe=kaalia_recipe, user=end_user)
        two_kgs_onions_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=onions, recipe=kaalia_recipe, user=end_user)
        one_kgs_pistachio_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=1, unit=kilograms, ingredient=pistachio, recipe=kaalia_recipe, user=end_user)
        one_litres_milk_in_kaalia = RecipeIngredient.objects.get_or_create(quantity=1, unit=litres, ingredient=milk, recipe=kaalia_recipe, user=end_user)
        classify_recipe(kaalia_recipe)

        # Create or update Lentil recipe
        lentil_recipe, _ = Recipe.objects.update_or_create(
            title='lentil',
            defaults={'description': 'lentil', 'user': end_user}
        )

        # Create or update MethodStep objects (global)
        lentil_step1, _ = MethodStep.objects.update_or_create(
            step_number=1,
            method_text="Soak the lentils overnight"
        )

        lentil_step2, _ = MethodStep.objects.update_or_create(
            step_number=2,
            method_text="Dice the onions"
        )

        lentil_step3, _ = MethodStep.objects.update_or_create(
            step_number=3,
            method_text="Dice the garlic"
        )

        # Link steps to the recipe via ManyToMany
        lentil_recipe.method_steps.set([lentil_step1, lentil_step2, lentil_step3])

        one_kgs_lentil_in_lentil = RecipeIngredient.objects.get_or_create(quantity=2, unit=kilograms, ingredient=lentil, recipe=lentil_recipe, user=end_user)
        one_litre_water_in_lentil = RecipeIngredient.objects.get_or_create(quantity=1, unit=litres, ingredient=water, recipe=lentil_recipe, user=end_user)
        two_units_onions_in_lentil = RecipeIngredient.objects.get_or_create(quantity=2, unit=units, ingredient=onions, recipe=lentil_recipe, user=end_user)
        one_units_garlic_in_lentil = RecipeIngredient.objects.get_or_create(quantity=1, unit=units, ingredient=garlic, recipe=lentil_recipe, user=end_user)
        classify_recipe(lentil_recipe)


