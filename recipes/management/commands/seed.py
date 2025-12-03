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
from django.core.management.base import BaseCommand, CommandError
from recipes.models import User, Tag, MethodStep, Recipe


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
            {"name": "Dairy-free", "colour": "#f67fcb"}
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


    def create_users(self):
        """
        Create fixture users and then generate random users up to USER_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on username/email) are ignored and generation continues.
        """
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
            try:
                Tag.objects.create(name=tag["name"], colour=tag["colour"])
            except:
                pass
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