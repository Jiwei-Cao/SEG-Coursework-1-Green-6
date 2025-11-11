from django.core.management.base import BaseCommand, CommandError
from recipes.models import User

class Command(BaseCommand):
    """
    Management command to remove (unseed) user data from the database.

    This command deletes all non-staff users from the database. It is designed
    to complement the corresponding "seed" command, allowing developers to
    reset the database to a clean state without removing administrative users.

    Attributes:
        help (str): Short description displayed when running
            `python manage.py help unseed`.
    """
    
    help = 'Seeds the database with sample data'

    def handle(self, *args, **options):
        """
        Execute the unseeding process.

        Deletes all `User` records where `is_staff` is False, preserving
        administrative accounts. Prints a confirmation message upon completion.

        Args:
            *args: Positional arguments passed by Django (not used here).
            **options: Keyword arguments passed by Django (not used here).

        Returns:
            None
        """

        User.objects.filter(is_staff=False).delete()