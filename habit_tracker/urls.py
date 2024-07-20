from django.urls import path, include


from habit_tracker.views import (
    index,
    my_profile,
    HabitsListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("all-habits/", HabitsListView.as_view(), name="my-habits"),
    path("my_profile/", my_profile, name="my-profile"),
]

app_name = "habit_tracker"
