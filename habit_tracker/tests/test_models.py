# from django.test import TestCase
# from habit_tracker.models import User, Habit, UserHabit, UserHabitDetail
#
#
# class TestModels(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(
#             username="johnny12",
#             password="John1234"
#         )
#
#         self.habit = Habit.objects.create(
#             name="Morning Boost",
#             description="Start each day with a quick physical routine to energize yourself for the day ahead."
#         )
#
#         self.user_habit = UserHabit.objects.create(
#             user=self.user,
#             habit=self.habit,
#             completed_per_day=3,
#             times_per_day=5
#         )
#
#         self.user_habit_detail = UserHabitDetail.objects.create(
#             user_habit=self.user_habit,
#             days_to_achieve=10
#         )
#
#     def test_habit_str(self):
#         expected = f"{self.habit.name} {self.habit.description}"
#         self.assertEqual(str(self.habit), expected)
#
#     def test_user_str(self):
#         expected = f"johnny12 (ID: {self.user.id})"
#         self.assertEqual(str(self.user), expected)
#
#     def test_user_habit_str(self):
#         expected = f"{self.user_habit.user} {self.user_habit.habit.name} {self.user_habit.date_of_assign}"
#         self.assertEqual(str(self.user_habit), expected)
#
#     def test_user_habit_save(self):
#         self.assertIsNotNone(self.user_habit.date_of_assign)
#
#     def test_not_enough_completed_times(self):
#         expected_times_per_day = 5
#         completed = self.user_habit.completed_per_day
#         self.assertLess(completed, expected_times_per_day)
#
#     def test_enough_completed_times(self):
#         initial_days_to_achieve = self.user_habit_detail.days_to_achieve
#         self.user_habit.completed_per_day = 5
#         self.user_habit_detail.completed_with_times_per_day()
#         expected_days_to_achieve = initial_days_to_achieve - 1
#         self.assertEqual(expected_days_to_achieve, self.user_habit_detail.days_to_achieve)
#
#     def test_achieved_habit_true(self):
#         self.user_habit_detail.days_to_achieve = 0
#         self.user_habit_detail.achieved_habit_is_true()
#         self.assertTrue(self.user_habit_detail.achieved_habit)
#
#     def test_achieved_habit_false(self):
#         self.user_habit_detail.days_to_achieve = 14
#         self.user_habit_detail.achieved_habit_is_true()
#         self.assertFalse(self.user_habit_detail.achieved_habit)
#
#     def test_completed_with_times_per_day_increase_days_to_achieve(self):
#         self.user_habit.completed_per_day = 5
#         initial_days_to_achieve = self.user_habit_detail.days_to_achieve
#         self.user_habit_detail.completed_with_times_per_day()
#         expected_days_to_achieve = initial_days_to_achieve - 1
#         self.assertEqual(expected_days_to_achieve, self.user_habit_detail.days_to_achieve)
#
#     def test_completed_with_times_per_day_not_increase_days_to_achieve(self):
#         self.user_habit.completed_per_day = 3
#         initial_days_to_achieve = self.user_habit_detail.days_to_achieve
#         self.user_habit_detail.completed_with_times_per_day()
#         self.assertEqual(initial_days_to_achieve, self.user_habit_detail.days_to_achieve)
