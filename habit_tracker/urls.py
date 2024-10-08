from django.contrib import admin
from django.urls import (
    path,
    include
)
from habit_tracker.views import (
    IndexView,
    MyProfileView,
    MyHabitsListView,
    confirm_operation,
    complete_operation,
    HabitListView,
    HabitCreateView,
    HabitUpdateView,
    assign_habit_to_user,
    RegisterView,
    UserHabitDetailUpdateView,
    remove_habit_from_user,
    HabitDetailCreateView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/admin/', admin.site.urls),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path("my_habits/", MyHabitsListView.as_view(), name="my-habits"),
    path("my_habits/create_my_habit", HabitDetailCreateView.as_view(), name="my-habits-create"),
    path("my_habits/<int:pk>/edit/", UserHabitDetailUpdateView.as_view(), name="my-habits-update"),
    path("all_habits/", HabitListView.as_view(), name="all-habits"),
    path("all_habits/create_habit/", HabitCreateView.as_view(), name="create-habit"),
    path("all_habits/<int:pk>/assign_habit/", assign_habit_to_user, name="assign-habit"),
    path("all_habits/<int:pk>/remove_from_my_list/", remove_habit_from_user, name="remove-habit"),
    path("all_habits/<int:pk>/update_habit/", HabitUpdateView.as_view(), name="update-habit"),
    path("my_profile/", MyProfileView.as_view(), name="my-profile"),
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
]

app_name = "habit_tracker"
