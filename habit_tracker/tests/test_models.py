from django.test import TestCase
from django.contrib.auth import get_user_model

from habit_tracker.models import (
    Habit,
    UserHabit,
    UserHabitDetail
)

User = get_user_model()


class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="randomuser123", password="randompassword456")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "randomuser123")

    def test_user_str(self):
        self.assertEqual(str(self.user), "randomuser123 (ID: 1)")

    def test_habit_creation(self):
        habit = Habit.objects.create(name="Drink Water", description="Drink 8 glasses of water daily")
        self.assertEqual(habit.name, "Drink Water")
        self.assertEqual(habit.description, "Drink 8 glasses of water daily")

    def test_habit_str(self):
        habit = Habit.objects.create(name="Exercise", description="Morning exercises for 30 minutes")
        self.assertEqual(str(habit), "Exercise Morning exercises for 30 minutes")

    def test_user_habit_creation(self):
        habit = Habit.objects.create(name="Read Books", description="Read one book per week")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(user_habit.user, self.user)
        self.assertEqual(user_habit.habit, habit)

    def test_user_habit_str(self):
        habit = Habit.objects.create(name="Meditate", description="Meditate for 10 minutes daily")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(str(user_habit), "Meditate (Date of assign: {})".format(user_habit.date_of_assign))

    def test_user_habit_default_date(self):
        habit = Habit.objects.create(name="Yoga", description="Practice yoga thrice a week")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_creation(self):
        habit = Habit.objects.create(name="Jogging", description="Jogging for 5 kilometers daily")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=25)
        self.assertEqual(user_habit_detail.user_habit, user_habit)
        self.assertEqual(user_habit_detail.days_to_achieve, 25)

    def test_user_habit_detail_default_values(self):
        habit = Habit.objects.create(name="Healthy Eating", description="Follow a balanced diet")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertEqual(user_habit_detail.days_to_achieve, 21)
        self.assertFalse(user_habit_detail.skip_day)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_user_habit_detail_str(self):
        habit = Habit.objects.create(name="Reading", description="Read for 30 minutes before bed")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=15)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), "No")

    def test_user_habit_detail_achieved_habit(self):
        habit = Habit.objects.create(name="Gardening", description="Spend time in the garden daily")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=0)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), "Yes")

    def test_habit_ordering(self):
        Habit.objects.create(name="C Habit", description="Description 3")
        Habit.objects.create(name="A Habit", description="Description 1")
        habits = Habit.objects.all()
        self.assertEqual(habits[0].name, "A Habit")
        self.assertEqual(habits[1].name, "C Habit")

    def test_user_habit_date_of_assign(self):
        habit = Habit.objects.create(name="Swimming", description="Swim for an hour twice a week")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_days_to_achieve(self):
        habit = Habit.objects.create(name="Painting", description="Paint one picture every month")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.days_to_achieve, 30)

    def test_user_habit_detail_skip_day_default(self):
        habit = Habit.objects.create(name="Cycling", description="Cycle for 20 kilometers every weekend")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.skip_day)

    def test_user_habit_detail_achieved_habit_default(self):
        habit = Habit.objects.create(name="Playing Guitar", description="Practice guitar daily for 1 hour")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_user_habit_detail_achieved_habit_method(self):
        habit = Habit.objects.create(name="Writing", description="Write a journal entry daily")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=0)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), "Yes")

    def test_user_habit_detail_achieved_habit_is_false(self):
        habit = Habit.objects.create(name="Photography", description="Take one photo every day")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), "No")

    def test_user_habit_foreign_key(self):
        habit = Habit.objects.create(name="Hiking", description="Go hiking once a month")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(user_habit.habit, habit)

    def test_user_habit_detail_one_to_one_field(self):
        habit = Habit.objects.create(name="Sketching", description="Sketch one drawing every week")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertEqual(user_habit_detail.user_habit, user_habit)

    def test_user_habit_null_date(self):
        habit = Habit.objects.create(name="Cooking", description="Cook a new recipe every week")
        user_habit = UserHabit(user=self.user, habit=habit, date_of_assign=None)
        user_habit.save()
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_blank_fields(self):
        habit = Habit.objects.create(name="Running", description="Run 5 kilometers every morning")
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.skip_day)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_habit_ordering_by_name(self):
        Habit.objects.create(name="Fishing", description="Go fishing every weekend")
        Habit.objects.create(name="Dancing", description="Dance for 30 minutes daily")
        Habit.objects.create(name="Journaling", description="Write a daily journal")
        habits = Habit.objects.all()
        self.assertEqual(habits[0].name, "Dancing")
        self.assertEqual(habits[1].name, "Fishing")
