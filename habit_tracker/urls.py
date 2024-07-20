from django.urls import path, include


from habit_tracker.views import (
    index,
    my_profile,
    HabitsListView, my_habits,
)


urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("may_habits", my_habits, name="my-habits"),
    path("all_habits/", HabitsListView.as_view(), name="all-habits"),
    path("my_profile/", my_profile, name="my-profile"),
]

app_name = "habit_tracker"
