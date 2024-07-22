from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    username = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"{self.username} (ID: {self.id})"


class Habit(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)

    class Meta:
        ordering = ("name", )

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
        return f"{self.habit.name} (Date of assign: {self.date_of_assign})"


class UserHabitDetail(models.Model):
    user_habit = models.OneToOneField("UserHabit", on_delete=models.CASCADE)
    days_to_achieve = models.IntegerField(default=21, blank=True, null=True, validators=[MinValueValidator(1)])
    skip_day = models.BooleanField(default=False, editable=False, blank=True, null=True)
    achieved_habit = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ("-user_habit__date_of_assign", )

    def achieved_habit_is_true(self):
        if self.days_to_achieve < 1:
            return "Yes"
        else:
            return "No"
