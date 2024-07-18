from django.urls import path

from habit_tracker.views import index


urlpatterns = [
    path("", index, name="index"),
]
