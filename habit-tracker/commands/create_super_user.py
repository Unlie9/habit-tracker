from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a superuser if none exist'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin12344321Q'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created new superuser'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
