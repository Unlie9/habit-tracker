import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project-service.settings')
django.setup()

# Применяем миграции
call_command("migrate")

# Создаем суперпользователя
call_command("create_superuser")

# Загружаем данные из фикстуры
call_command("loaddata", "data.json")
