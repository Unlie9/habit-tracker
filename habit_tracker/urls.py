from django.urls import path, include


from habit_tracker.views import (
    index,
    my_profile,
    HabitsListView,
    HabitAssignView,
    HabitCreateView,
    HabitDetailView, HabitDeleteView, HabitUpdateView,

)


urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("all-habits/", HabitsListView.as_view(), name="all-habits"),
    path("all_habits/create_habit/", HabitCreateView.as_view(), name="all-habits-create"),
    path("all-habits/assign_habit/<int:id>/", HabitAssignView.as_view(), name="assign-habit"),
    path("all_habits/update-habit/<int:id>/", HabitUpdateView.as_view(), name="update-habit"),
    path("all_habits/delete-habit/<int:id>/", HabitDeleteView.as_view(), name="delete-habit"),
    path("my_profile/", my_profile, name="my-profile"),
]

app_name = "habit_tracker"
