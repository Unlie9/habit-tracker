import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from habit_tracker.models import (
    User,
    Habit
)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if not username.isalnum():
            raise forms.ValidationError(
                "Username must contain only alphanumeric characters.",
                code="invalid",
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email address is already in use.")
        return email


class HabitForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 2, "cols": 19}
        )
    )

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

        if not re.fullmatch(r'[a-zA-Z\s\(\)]+', name):
            errors['name'] = "Name must contain only letters, spaces, and parentheses."

        if not re.fullmatch(r'[a-zA-Z0-9\s]+', description):
            errors['description'] = "Description must contain only alphanumeric characters and spaces."

        if len(name) > 28:
            errors['name'] = "Name must be less than 28 characters."

        if len(description) > 30:
            errors['description'] = "Description must be less than 30 characters."

        if errors:
            raise ValidationError(errors)

        return cleaned_data


class DeleteHabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = []


class HabitSearchForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        ),
    )




