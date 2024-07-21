from django.urls import path, include
from habit_tracker.views import (
    index,
    my_profile,
    my_habits,
    confirm_operation,
    complete_operation,
    HabitListView,
    HabitCreateView,
    HabitUpdateView,
    HabitDeleteView,
    AssignHabitView,
    RegisterView,
    UserHabitDetailUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('register/', RegisterView.as_view(), name='register'),
    path(
        "confirm/update_days_to_achieve/<int:detail_id>/<str:operation>/",
        confirm_operation,
        name="confirm_operation"
    ),
    path(
        "complete/update_days_to_achieve/<int:detail_id>/<str:operation>/",
        complete_operation,
        name="complete_operation"
    ),
    path("my_habits/", my_habits, name="my-habits"),
    path("my_habits/<int:pk>/edit/", UserHabitDetailUpdateView.as_view(), name="my-habits-update"),
    path("all_habits/", HabitListView.as_view(), name="all-habits"),
    path("all_habits/create_habit/", HabitCreateView.as_view(), name="create-habit"),
    path("all_habits/<int:pk>/assign_habit/", AssignHabitView.as_view(), name="assign-habit"),
    path("all_habits/<int:pk>/update_habit/", HabitUpdateView.as_view(), name="update-habit"),
    path("all_habits/<int:pk>/delete_habit/", HabitDeleteView.as_view(), name="delete-habit"),
    path("my_profile/", my_profile, name="my-profile"),
]

app_name = "habit_tracker"
