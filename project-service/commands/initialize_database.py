import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project-service.settings')
django.setup()


call_command("migrate")

call_command("create_superuser")

call_command("loaddata", "data.json")
