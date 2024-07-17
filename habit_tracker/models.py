from django.utils import timezone
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True)


class Habit(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    times_per_day = models.IntegerField()
    days_to_achieve = models.IntegerField()


class UserHabit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habit = models.ForeignKey("Habit", on_delete=models.CASCADE)
    date_finish = models.DateField()
    current_date = models.DateField()
    date_of_assign = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_date = timezone.now()
            self.date_finish = self.current_date + timedelta(days=self.habit.days_to_achieve)


class UserHabitDetail(models.Model):
    user_habit = models.OneToOneField("UserHabit", on_delete=models.CASCADE)
    skip_day = models.BooleanField()
    achieved_habit = models.BooleanField()
    completed_per_day = models.IntegerField()
