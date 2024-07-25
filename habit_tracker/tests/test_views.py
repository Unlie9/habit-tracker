from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from habit_tracker.models import (
    Habit,
    UserHabit,
    UserHabitDetail
)

User = get_user_model()
client = Client()


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = client
        self.user = User.objects.create_user(username="testuser1", password="password1")
        self.habit1 = Habit.objects.create(name="Exercise", description="Morning exercise")
        self.habit2 = Habit.objects.create(name="Reading", description="Read every day")
        self.user_habit1 = UserHabit.objects.create(user=self.user, habit=self.habit1)
        self.user_habit2 = UserHabit.objects.create(user=self.user, habit=self.habit2)
        self.client.login(username="testuser1", password="password1")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.context["user"], self.user)
        self.assertIn("user_habits", response.context)
        self.assertIn("num_user_habits", response.context)

    def test_index_view_num_visits(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(self.client.session["num_visits"], 1)


class HabitListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser2", password="password2")
        self.habit1 = Habit.objects.create(name="Exercise", description="Morning exercise")
        self.habit2 = Habit.objects.create(name="Reading", description="Read every day")
        self.habit3 = Habit.objects.create(name="Meditation", description="Daily meditation")
        self.user_habit = UserHabit.objects.create(user=self.user, habit=self.habit1)
        self.client.login(username="testuser2", password="password2")

    def test_habit_list_view_status_code(self):
        response = self.client.get(reverse("all-habits"))
        self.assertEqual(response.status_code, 200)

    def test_habit_list_view_context(self):
        response = self.client.get(reverse("all-habits"))
        self.assertIn("habits_list", response.context)
        self.assertIn("user_habits", response.context)
        self.assertIn("num_habits", response.context)

    def test_habit_list_view_search(self):
        response = self.client.get(reverse("all-habits"), {"name": "Meditation"})
        self.assertContains(response, "Meditation")
        self.assertNotContains(response, "Exercise")


class HabitCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser3", password="password3")
        self.client.login(username="testuser3", password="password3")

    def test_habit_create_view_status_code(self):
        response = self.client.get(reverse("create-habit"))
        self.assertEqual(response.status_code, 200)

    def test_habit_create_view_form_valid(self):
        response = self.client.post(reverse("create-habit"), {
            "name": "New Habit",
            "description": "This is a new habit"
        })
        self.assertRedirects(response, reverse("all-habits"))
        self.assertTrue(Habit.objects.filter(name="(global habit) New Habit").exists())


class HabitUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser4", password="password4")
        self.habit = Habit.objects.create(name="Exercise", description="Morning exercise")
        self.client.login(username="testuser4", password="password4")

    def test_habit_update_view_status_code(self):
        response = self.client.get(reverse("update-habit", kwargs={"pk": self.habit.pk}))
        self.assertEqual(response.status_code, 200)

    def test_habit_update_view_form_valid(self):
        response = self.client.post(reverse("update-habit", kwargs={"pk": self.habit.pk}), {
            "name": "Updated Habit",
            "description": "Updated description"
        })
        self.assertRedirects(response, reverse("my-habits"))
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, "Updated Habit")
        self.assertEqual(self.habit.description, "Updated description")


class AssignHabitToUserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser5", password="password5")
        self.habit = Habit.objects.create(name="Exercise", description="Morning exercise")
        self.client.login(username="testuser5", password="password5")

    def test_assign_habit_to_user(self):
        response = self.client.post(reverse("assign-habit", kwargs={"pk": self.habit.pk}))
        self.assertRedirects(response, reverse("all-habits"))
        user_habit = UserHabit.objects.get(user=self.user, habit=self.habit)
        self.assertTrue(UserHabitDetail.objects.filter(user_habit=user_habit).exists())


class CompleteOperationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser6", password="password6")
        self.habit = Habit.objects.create(name="Exercise", description="Morning exercise")
        self.user_habit = UserHabit.objects.create(user=self.user, habit=self.habit)
        self.user_habit_detail = UserHabitDetail.objects.create(user_habit=self.user_habit, days_to_achieve=10)
        self.client.login(username="testuser6", password="password6")

    def test_complete_operation_completed(self):
        response = self.client.post(reverse("complete_operation", kwargs={"detail_id": self.user_habit_detail.id, "operation": "completed"}))
        self.user_habit_detail.refresh_from_db()
        self.assertEqual(self.user_habit_detail.days_to_achieve, 9)
        self.assertFalse(self.user_habit_detail.skip_day)
        self.assertRedirects(response, reverse("index"))

    def test_complete_operation_reset(self):
        response = self.client.post(reverse("complete_operation", kwargs={"detail_id": self.user_habit_detail.id, "operation": "reset"}))
        self.user_habit_detail.refresh_from_db()
        self.assertEqual(self.user_habit_detail.days_to_achieve, 21)
        self.assertFalse(self.user_habit_detail.skip_day)
        self.assertRedirects(response, reverse("index"))
