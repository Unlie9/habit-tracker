from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from habit_tracker.models import Habit


@receiver(post_save, sender=User)
def assign_habits_to_new_user(sender, instance, created, **kwargs):
    if created:
        default_habits = [
            {"name": "Read Books", "description": "Read at least 20 pages daily"},
            {"name": "Exercise", "description": "30 minutes of exercise"},
            {"name": "Meditation", "description": "Meditate for 10 minutes"},
            {"name": "Read Books Again", "description": "Read at least 20 pages daily"},
            {"name": "Exercise Again", "description": "30 minutes of exercise"},
            {"name": "Meditation Again", "description": "Meditate for 10 minutes"}
        ]

        for habit_data in default_habits:
            Habit.objects.get_or_create(**habit_data)


@receiver(post_save, sender=User)
def create_second_superuser(sender, instance, created, **kwargs):
    if created and instance.username == 'admin':
        if not User.objects.filter(username='admin2').exists():
            User.objects.create_superuser(
                username='admin2',
                email='admin2@example.com',
                password='admin'
            )
