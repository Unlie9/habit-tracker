import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")
        errors = {}

        if not name or not description:
            return cleaned_data

        if not re.fullmatch(r'[a-zA-Z]+', name):
            errors['name'] = "Name must contain only letters."

        if not re.fullmatch(r'[a-zA-Z0-9]+', description):
            errors['description'] = "Description must contain only alphanumeric characters."

        if len(name) > 16:
            errors['name'] = "Name must be less than 16 characters."

        if len(description) > 40:
            errors['description'] = "Description must be less than 40 characters."

        if errors:
            raise ValidationError(errors)

        return cleaned_data


class DeleteHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = []
