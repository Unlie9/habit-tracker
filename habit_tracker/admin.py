from django.contrib import admin
from .models import (
    User,
    Habit,
    UserHabit,
    UserHabitDetail
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_active")
    ordering = ("username",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)


@admin.register(UserHabit)
class UserHabitAdmin(admin.ModelAdmin):
    list_display = ("user", "habit", "date_of_assign")
    search_fields = ("user__username", "habit__name")
    list_filter = ("date_of_assign",)
    ordering = ("-date_of_assign",)


@admin.register(UserHabitDetail)
class UserHabitDetailAdmin(admin.ModelAdmin):
    list_display = ("user_habit", "days_to_achieve", "skip_day", "achieved_habit_is_true")
    search_fields = ("user_habit__user__username", "user_habit__habit__name")
    list_filter = ("days_to_achieve", "skip_day", "achieved_habit")
    ordering = ("-user_habit__date_of_assign",)

    def achieved_habit_is_true(self, obj):
        return "Yes" if obj.days_to_achieve < 1 else "No"
    achieved_habit_is_true.short_description = "Achieved"
