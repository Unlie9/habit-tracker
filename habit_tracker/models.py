from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    username = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"{self.username} (ID: {self.id})"


class Habit(models.Model):
    name = models.CharField(max_length=50, editable=False)
    description = models.CharField(max_length=120, editable=False)

    def __str__(self):
        return f"{self.name} {self.description}"


class UserHabit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    habit = models.ForeignKey("Habit", on_delete=models.CASCADE)
    date_of_assign = models.DateField(auto_now_add=True, null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.date_of_assign = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} {self.habit.name} {self.date_of_assign}"


class UserHabitDetail(models.Model):
    user_habit = models.OneToOneField("UserHabit", on_delete=models.CASCADE)
    times_per_day = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    days_to_achieve = models.IntegerField(default=21, blank=True, null=True, validators=[MinValueValidator(1)])
    skip_day = models.BooleanField(default=False, editable=False, blank=True, null=True)
    achieved_habit = models.BooleanField(default=False, editable=False, blank=True, null=True)
    completed_per_day = models.IntegerField()

    def completed_with_times_per_day(self):
        self.skip_day = self.completed_per_day < self.times_per_day

        if not self.skip_day:
            self.days_to_achieve -= 1

        self.completed_per_day = 0

        self.user_habit.save()
        self.user_habit.habit.save()

    def achieved_habit_is_true(self):
        if self.days_to_achieve == 0:
            self.achieved_habit = True
            self.save()
