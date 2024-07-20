from django.urls import path, include
from habit_tracker.views import (
    index,
    my_profile,
    HabitsListView,
    my_habits,
    confirm_operation,
    complete_operation
)

urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
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
    path("all_habits/", HabitsListView.as_view(), name="all-habits"),
    path("my_profile/", my_profile, name="my-profile"),
]
app_name = "habit_tracker"
