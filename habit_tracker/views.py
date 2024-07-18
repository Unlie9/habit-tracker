from django.shortcuts import render

from habit_tracker.models import (
    Habit,
    User,
    UserHabitDetail,
    UserHabit
)


# @login_required
def index(request):
    """View function for the home page of the site."""

    num_habits = Habit.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_habits": num_habits,
        "num_visits": num_visits + 1,
    }

    return render(request, "habit_tracker/index.html", context=context)
