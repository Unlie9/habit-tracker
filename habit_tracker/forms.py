from django import forms
from django.contrib.auth.forms import UserCreationForm

from habit_tracker.models import User, Habit


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "username",
            "password1",
            "password2",
        )

    def clean_username(self):
        username = self.cleaned_data["username"]

        if not username.isalnum():
            raise forms.ValidationError(
                "Username must contain only alphanumeric characters.",
                code="invalid",
            )
        return username


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["name", "description"]
