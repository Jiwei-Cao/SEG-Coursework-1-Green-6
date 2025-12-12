"""
Management command to seed the database with demo data.

This command creates a small set of named fixture users and then fills up
to ``USER_COUNT`` total users using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""

from faker import Faker
from faker.providers import company
from faker_food import FoodProvider
from random import randint, random
from django.core.management.base import BaseCommand
from recipes.models import User, Tag, MethodStep, Recipe, RecipeIngredient, Ingredient, Unit, Comment
from django.utils.timezone import make_aware
import datetime


user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

tag_fixtures = [
            {"name": "Vegan", "colour": "#2f88ff"}, 
            {"name": "Vegetarian", "colour": "#0d96b6"},
            {"name": "Gluten-free", "colour": "#d59d4d"},
            {"name": "Quick", "colour":"#b26459"},
            {"name": "Easy", "colour": "#b26459"},
            {"name": "Mediterranean", "colour": "#e9dfec"},
            {"name": "Asian", "colour": "#b3a496"},
            {"name": "Indian", "colour": "#82ae67"},
            {"name": "Dairy-free", "colour": "#f67fcb"},
            {"name": "Nut-free", "colour":"#e8cc2b"}
        ]

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

    USER_COUNT = 200
    RECIPE_COUNT = 30
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker('en_GB')
        self.faker.add_provider(FoodProvider)
        self.faker.add_provider(company.Provider)

    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.users`` for any
        post-processing or debugging (not required for operation).
        """
        self.create_users()
        self.users = User.objects.all()
        self.create_tags()
        self.create_recipes()
        self.create_units()
        self.create_ingredients()
        self.create_recipeingredients()

    def add_arguments(self, parser):
        parser.add_argument('flag', type=str, nargs='?', default='retain')

    def create_users(self):
        """
        Create fixture users and then generate random users up to USER_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
        User.objects.create_superuser('@johndoe', 'john.doe@example.org', 'Password123')
        self.generate_user_fixtures()
        self.generate_random_users()


    def generate_user_fixtures(self):
        """Attempt to create each predefined fixture user."""
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        """
        Generate random users until the database contains USER_COUNT users.

        Prints a simple progress indicator to stdout during generation.
        """
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        """
        Generate a single random user and attempt to insert it.

        Uses Faker for first/last names, then derives a simple username/email.
        """
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        """
        Attempt to create a user and ignore any errors.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        """
        Create a user with the default password.

        Args:
            data (dict): Mapping with keys ``username``, ``email``,
                ``first_name``, and ``last_name``.
        """
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
    
    def create_tags(self):
        """Construct default tags for the Tag Model"""
        for tag in tag_fixtures:
            tag_object, created = Tag.objects.get_or_create(
                name=tag["name"],
                defaults={"colour": tag["colour"]}
            )

        # If the tag already existed, update its colour
            if not created:
                tag_object.colour = tag["colour"]
                tag_object.save()
        print("Tag seeding complete")
        
    def create_recipes(self):
        for i in range(self.RECIPE_COUNT):
            for user in user_fixtures:
                data={}
                data["user"] = User.objects.get(username=user["username"])
                data["title"] = self.faker.dish()
                data["description"] = self.faker.dish_description()
                data["tags"] = self.create_tag_list()
                data["method"] = self.create_method()
                data["comments"] = self.create_comments(user)
                create_recipe(data)

    def create_tag_list(self):
        num_tags = self.faker.random_int(0,len(tag_fixtures))
        tags = []
        for i in range(num_tags):
            tag = Tag.objects.get(name=tag_fixtures[i]["name"])
            tags.append(tag)
        return tags
    
    def create_method(self):
        num_steps = self.faker.random_int(1,20)
        method_steps = []
        for i in range(1,num_steps):
            method_text = f"Add {self.faker.measurement()} {self.faker.ingredient()}."
            method_steps.append(MethodStep.objects.create(method_text=method_text, step_number=i))
        return method_steps

    def create_comments(self, user):
        num_comments = self.faker.random_int(1, 20)
        comments = []
        for i in range(1, num_comments):
            username = User.objects.get(username=user_fixtures[self.faker.random_int(0, len(user_fixtures)-1)]["username"])
            comment =  self.faker.sentence(nb_words=5)
            date_published = self.faker.date_time_between_dates(datetime_start="-5y", datetime_end="now")
            comment_object = Comment.objects.create(user=username, comment=comment, date_published=date_published)
            replies = self.create_replies(comment_object)
            comment_object.replies.set(replies)
            comments.append(comment_object)
        return comments

    def create_replies(self, comment_object):
        num_replies = self.faker.random_int(1, 10)
        replies = []
        for i in range(1, num_replies):
            username = User.objects.get(username=user_fixtures[self.faker.random_int(0, len(user_fixtures)-1)]["username"])
            comment =  self.faker.sentence(nb_words=5)
            date_published = self.faker.date_time_between_dates(datetime_start=comment_object.date_published, datetime_end="now")
            replies.append(Comment.objects.create(user=username, comment=comment, date_published=date_published))
        return replies

    
    def create_units(self):
        end_user = User.objects.get(username='@johndoe')
        Unit.objects.create(name='kilograms', symbol='kgs', user=end_user)
        Unit.objects.create(name='pounds', symbol='lbs', user=end_user)
        Unit.objects.create(name='teaspoons', symbol='tsps', user=end_user)
        Unit.objects.create(name='tablespoons', symbol='tbsps', user=end_user)
        Unit.objects.create(name='litres', symbol='ltrs', user=end_user)
        Unit.objects.create(name='millilitres', symbol='mls', user=end_user)
        Unit.objects.create(name='grams', symbol='gs', user=end_user)
        Unit.objects.create(name='units', symbol='units', user=end_user)

    def create_ingredients(self):
        end_user = User.objects.get(username='@johndoe')
        # Ingredients
        Ingredient.objects.create(name='beef', category=Ingredient.BUTCHERY, user=end_user)
        Ingredient.objects.create(name='potato', category=Ingredient.VEGETABLE, user=end_user)
        Ingredient.objects.create(name='rice', category=Ingredient.GRAINS, user=end_user)
        Ingredient.objects.create(name='chicken', category=Ingredient.BUTCHERY, user=end_user)
        Ingredient.objects.create(name='pork', category=Ingredient.BUTCHERY, user=end_user)
        Ingredient.objects.create(name='lamb', category=Ingredient.BUTCHERY, user=end_user)
        Ingredient.objects.create(name='onions', category=Ingredient.ALLUM, user=end_user)
        Ingredient.objects.create(name='garlic', category=Ingredient.ALLUM, user=end_user)
        Ingredient.objects.create(name='flour',category=Ingredient.MINERALS, user=end_user)
        Ingredient.objects.create(name='salt', category=Ingredient.MINERALS, user=end_user)
        Ingredient.objects.create(name='sugar', category=Ingredient.MINERALS, user=end_user)
        Ingredient.objects.create(name='pepper', category=Ingredient.SPICE, user=end_user)
        Ingredient.objects.create(name='cinnamon', category=Ingredient.SPICE, user=end_user)
        Ingredient.objects.create(name='pistachio', category=Ingredient.NUT, user=end_user)
        Ingredient.objects.create(name='almond', category=Ingredient.NUT, user=end_user)
        Ingredient.objects.create(name='lentil', category=Ingredient.PULSES, user=end_user)
        Ingredient.objects.create(name='water', category=Ingredient.WATER, user=end_user)
        Ingredient.objects.create(name='milk', category=Ingredient.DAIRY, user=end_user)
        Ingredient.objects.create(name='tomato', category=Ingredient.VEGETABLE, user=end_user)
        Ingredient.objects.create(name='carrot', category=Ingredient.VEGETABLE, user=end_user)
        Ingredient.objects.create(name='celery', category=Ingredient.VEGETABLE, user=end_user) 
        Ingredient.objects.create(name='bell pepper', category=Ingredient.VEGETABLE, user=end_user) 
        Ingredient.objects.create(name='mushroom', category=Ingredient.VEGETABLE, user=end_user)
        Ingredient.objects.create(name='spinach', category=Ingredient.VEGETABLE, user=end_user) 
        Ingredient.objects.create(name='courgette', category=Ingredient.VEGETABLE, user=end_user) 
        Ingredient.objects.create(name='aubergine', category=Ingredient.VEGETABLE, user=end_user) 
        Ingredient.objects.create(name='shallot', category=Ingredient.ALLUM, user=end_user)
        Ingredient.objects.create(name='leek', category=Ingredient.ALLUM, user=end_user) 
        Ingredient.objects.create(name='basil', category=Ingredient.HERBS, user=end_user) 
        Ingredient.objects.create(name='parsley', category=Ingredient.HERBS, user=end_user)
        Ingredient.objects.create(name='coriander', category=Ingredient.HERBS, user=end_user)
        Ingredient.objects.create(name='thyme', category=Ingredient.HERBS, user=end_user)
        Ingredient.objects.create(name='rosemary', category=Ingredient.HERBS, user=end_user)
        Ingredient.objects.create(name='dill', category=Ingredient.HERBS, user=end_user) 
        Ingredient.objects.create(name='cumin', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='turmeric', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='paprika', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='chili powder', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='nutmeg', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='cardamom', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='salmon', category=Ingredient.SEAFOOD, user=end_user) 
        Ingredient.objects.create(name='shrimp', category=Ingredient.SEAFOOD, user=end_user) 
        Ingredient.objects.create(name='tuna', category=Ingredient.SEAFOOD, user=end_user) 
        Ingredient.objects.create(name='egg', category=Ingredient.EGG, user=end_user) 
        Ingredient.objects.create(name='butter', category=Ingredient.DAIRY, user=end_user) 
        Ingredient.objects.create(name='cream', category=Ingredient.DAIRY, user=end_user) 
        Ingredient.objects.create(name='yogurt', category=Ingredient.DAIRY, user=end_user) 
        Ingredient.objects.create(name='cheese', category=Ingredient.DAIRY, user=end_user) 
        Ingredient.objects.create(name='pasta', category=Ingredient.GLUTEN, user=end_user) 
        Ingredient.objects.create(name='bread', category=Ingredient.GLUTEN, user=end_user) 
        Ingredient.objects.create(name='quinoa', category=Ingredient.GRAINS, user=end_user) 
        Ingredient.objects.create(name='chickpeas', category=Ingredient.PULSES, user=end_user) 
        Ingredient.objects.create(name='beans', category=Ingredient.PULSES, user=end_user) 
        Ingredient.objects.create(name='baking powder', category=Ingredient.MINERALS, user=end_user) 
        Ingredient.objects.create(name='baking soda', category=Ingredient.MINERALS, user=end_user) 
        Ingredient.objects.create(name='strawberry', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='banana', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='lemon', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='orange', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='apple', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='blueberry', category=Ingredient.FRUIT, user=end_user) 
        Ingredient.objects.create(name='honey', category=Ingredient.MINERALS, user=end_user) 
        Ingredient.objects.create(name='maple syrup', category=Ingredient.MINERALS, user=end_user) 
        Ingredient.objects.create(name='chocolate', category=Ingredient.MINERALS, user=end_user) 
        Ingredient.objects.create(name='cocoa powder', category=Ingredient.SPICE, user=end_user) 
        Ingredient.objects.create(name='vanilla', category=Ingredient.SPICE, user=end_user) 
                
    def create_recipeingredients(self):
        for recipe in Recipe.objects.all():
            end_user = User.objects.get(username='@johndoe')
            data={}
            data["user"] = end_user
            data["recipe"] = recipe
            data["quantity"] = 3
            data["unit"] = Unit.objects.get(pk=1)
            data["ingredient"] = Ingredient.objects.get(pk=2)
            create_recipeingredient(data)

def create_username(first_name, last_name):
    """
    Construct a simple username from first and last names.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.

    Returns:
        str: A username in the form ``@{firstname}{lastname}`` (lowercased).
    """
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    """
    Construct a simple example email address.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.

    Returns:
        str: An email in the form ``{firstname}.{lastname}@example.org``.
    """
    return first_name + '.' + last_name + '@example.org'

def create_recipe(data):
    recipe = Recipe.objects.create(
        user = data["user"],
        title = data["title"],
        description = data["description"]
        )
    recipe.tags.set(data["tags"])
    recipe.method_steps.set(data["method"])
    recipe.comments.set(data["comments"])

def create_recipeingredient(data):
    RecipeIngredient.objects.create(
        user = data["user"],
        recipe = data["recipe"],
        quantity = data["quantity"],
        unit = data["unit"],
        ingredient = data["ingredient"]
    )    

