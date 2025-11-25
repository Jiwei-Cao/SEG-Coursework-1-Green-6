"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to `USER_COUNT` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""


from recipes.models import Recipe, RecipeIngredient, RecipeMethod, Ingredient, Unit, User
from django.core.management.base import BaseCommand, CommandError
from recipes.models import User
class Command(BaseCommand):
    """
    Build automation command to seed the database with data.

    This command inserts a small set of known users (`user_fixtures`) and then
    repeatedly generates additional random users until `USER_COUNT` total users
    exist in the database. Each generated user receives the same default password.

    Attributes:
        USER_COUNT (int): Target total number of users in the database.
        DEFAULT_PASSWORD (str): Default password assigned to all created users.
        help (str): Short description shown in `manage.py help`.
        faker (Faker): Locale-specific Faker instance used for random data.
    """


    def _init_(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super()._init_(*args, **kwargs)


    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores `self.users` for any
        post-processing or debugging (not required for operation).
        """
        # Reset database except users
        Unit.objects.all().delete()
        Ingredient.objects.all().delete()
        Recipe.objects.all().delete()
        RecipeIngredient.objects.all().delete()
        RecipeMethod.objects.all().delete()

        admin_user = User.objects.get(username='@hbh')
        kilograms = Unit.objects.create(name='kilograms', symbol='kgs', user=admin_user)
        kilograms.save()
        pounds = Unit.objects.create(name='pounds', symbol='lbs', user=admin_user)
        pounds.save()
        teaspoons = Unit.objects.create(name='teaspoons', symbol='tsps', user=admin_user)
        teaspoons.save()
        tablespoons = Unit.objects.create(name='tablespoons', symbol='tbsps', user=admin_user)
        tablespoons.save()
        beef = Ingredient.objects.create(name='beef', category='BT', user=admin_user)
        beef.save()
        potato = Ingredient.objects.create(name='potato', category='VG', user=admin_user)
        potato.save()
        rice = Ingredient.objects.create(name='rice', category='CB', user=admin_user)
        rice.save()
        chicken = Ingredient.objects.create(name='chicken', category='BT', user=admin_user)
        chicken.save()
        lamb = Ingredient.objects.create(name='lamb', category='BT', user=admin_user)
        lamb.save()
        onions = Ingredient.objects.create(name='onions', category='VG', user=admin_user)
        onions.save()
        salt = Ingredient.objects.create(name='salt', category='HB', user=admin_user)
        salt.save()
        pepper = Ingredient.objects.create(name='pepper', category='HB', user=admin_user)
        pepper.save()
        biryani_recipe = Recipe.objects.create(title='Biryani', description='Biryani', user=admin_user)
        biryani_recipe.save()
        two_kgs_beef = RecipeIngredient.objects.create(quantity='2', unit=kilograms, ingredient=beef, recipe=biryani_recipe, user=admin_user)
        two_kgs_beef.save()
        two_kgs_potato = RecipeIngredient.objects.create(quantity='2', unit=kilograms, ingredient=potato, recipe=biryani_recipe, user=admin_user)
        two_kgs_potato.save()
        three_kgs_rice = RecipeIngredient.objects.create(quantity='3', unit=kilograms, ingredient=rice, recipe=biryani_recipe, user=admin_user)
        three_kgs_rice.save()
        biryani_step1 = RecipeMethod.objects.create(step='Cut the beef into cubes', order=10, recipe=biryani_recipe, user=admin_user)
        biryani_step1.save()
        biryani_step2 = RecipeMethod.objects.create(step='Cut the potato into quarters', order=20, recipe=biryani_recipe, user=admin_user)
        biryani_step2.save()
        biryani_step3 = RecipeMethod.objects.create(step='Soak the rice overnight', order=30, recipe=biryani_recipe, user=admin_user)
        biryani_step3.save()

        all_units = Unit.objects.all()
        all_ingredients = Ingredient.objects.all()
        all_recipes = Recipe.objects.all()
        all_recipe_ingredients = RecipeIngredient.objects.all()
        all_recipe_methods = RecipeMethod.objects.all()