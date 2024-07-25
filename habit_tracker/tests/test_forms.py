from django.test import TestCase
from django.contrib.auth import get_user_model

from habit_tracker.forms import (
    CustomUserCreationForm,
    HabitForm,
    DeleteHabitForm,
    HabitSearchForm
)

User = get_user_model()


class CustomUserCreationFormTests(TestCase):

    def test_invalid_username(self):
        form_data = {
            "username": "invalid user!",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
        self.assertEqual(form.errors["username"], ["Username must contain only alphanumeric characters."])

    def test_duplicate_email(self):
        User.objects.create_user(username="existinguser", email="john.doe@example.com", password="password123")
        form_data = {
            "username": "newuser",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password1": "password123",
            "password2": "password123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(form.errors["email"], ["Email address is already in use."])

    def test_password_widget_attributes(self):
        form = CustomUserCreationForm()
        self.assertEqual(form.fields['password1'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password1'].widget.attrs['placeholder'], 'Password')
        self.assertEqual(form.fields['password2'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['password2'].widget.attrs['placeholder'], 'Confirm Password')


class HabitFormTests(TestCase):

    def test_invalid_name(self):
        form_data = {
            "name": "Exercise123",
            "description": "Daily 30-minute jog",
        }
        form = HabitForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertEqual(form.errors["name"], ["Name must contain only letters, spaces, and parentheses."])

    def test_invalid_description(self):
        form_data = {
            "name": "Reading",
            "description": "Read books!!!",
        }
        form = HabitForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)
        self.assertEqual(form.errors["description"], ["Description must contain only alphanumeric characters and spaces."])

    def test_description_length(self):
        form_data = {
            "name": "Reading",
            "description": "A very long description that exceeds thirty characters",
        }
        form = HabitForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)
        self.assertEqual(form.errors["description"], ["Description must be less than 30 characters."])

    def test_description_widget_attributes(self):
        form = HabitForm()
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 2)
        self.assertEqual(form.fields['description'].widget.attrs['cols'], 19)


class DeleteHabitFormTests(TestCase):
    def test_form_fields(self):
        form = DeleteHabitForm()
        self.assertEqual(len(form.fields), 0)


class HabitSearchFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            "name": "Exercise",
        }
        form = HabitSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_search(self):
        form_data = {
            "name": "",
        }
        form = HabitSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_name_widget_attributes(self):
        form = HabitSearchForm()
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Search by name')
