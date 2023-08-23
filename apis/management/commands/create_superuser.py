from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser for deployment'

    def handle(self, *args, **options):
        username = os.environ.get('SUPERUSER_USERNAME','admin') # Set your desired superuser username
        email = os.environ.get('SUPERUSER_EMAIL')  # Set your desired superuser email
        password = os.environ.get('SUPERUSER_PASSWORD') # Set your desired superuser password

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
