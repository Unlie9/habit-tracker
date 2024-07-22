from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from habit_tracker.models import Habit, UserHabit, UserHabitDetail

User = get_user_model()


class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser (ID: 1)')

    def test_habit_creation(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        self.assertEqual(habit.name, 'Test Habit')
        self.assertEqual(habit.description, 'Test Description')

    def test_habit_str(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        self.assertEqual(str(habit), 'Test Habit Test Description')

    def test_user_habit_creation(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(user_habit.user, self.user)
        self.assertEqual(user_habit.habit, habit)

    def test_user_habit_str(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(str(user_habit), 'Test Habit (Date of assign: {})'.format(user_habit.date_of_assign))

    def test_user_habit_default_date(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_creation(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.user_habit, user_habit)
        self.assertEqual(user_habit_detail.days_to_achieve, 30)

    def test_user_habit_detail_default_values(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertEqual(user_habit_detail.days_to_achieve, 21)
        self.assertFalse(user_habit_detail.skip_day)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_user_habit_detail_str(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), 'No')

    def test_user_habit_detail_achieved_habit(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=0)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), 'Yes')

    def test_habit_ordering(self):
        Habit.objects.create(name='B Habit', description='Description 1')
        Habit.objects.create(name='A Habit', description='Description 2')
        habits = Habit.objects.all()
        self.assertEqual(habits[0].name, 'A Habit')
        self.assertEqual(habits[1].name, 'B Habit')

    def test_user_habit_date_of_assign(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_days_to_achieve(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.days_to_achieve, 30)

    def test_user_habit_detail_skip_day_default(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.skip_day)

    def test_user_habit_detail_achieved_habit_default(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_user_habit_detail_achieved_habit_method(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=0)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), 'Yes')

    def test_user_habit_detail_achieved_habit_is_false(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit, days_to_achieve=30)
        self.assertEqual(user_habit_detail.achieved_habit_is_true(), 'No')

    def test_user_habit_foreign_key(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        self.assertEqual(user_habit.habit, habit)

    def test_user_habit_detail_one_to_one_field(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertEqual(user_habit_detail.user_habit, user_habit)

    def test_user_habit_null_date(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit(user=self.user, habit=habit, date_of_assign=None)
        user_habit.save()
        self.assertIsNotNone(user_habit.date_of_assign)

    def test_user_habit_detail_blank_fields(self):
        habit = Habit.objects.create(name='Test Habit', description='Test Description')
        user_habit = UserHabit.objects.create(user=self.user, habit=habit)
        user_habit_detail = UserHabitDetail.objects.create(user_habit=user_habit)
        self.assertFalse(user_habit_detail.skip_day)
        self.assertFalse(user_habit_detail.achieved_habit)

    def test_habit_ordering_by_name(self):
        Habit.objects.create(name='Habit C', description='Description C')
        Habit.objects.create(name='Habit B', description='Description B')
        Habit.objects.create(name='Habit A', description='Description A')
        habits = Habit.objects.all()
        self.assertEqual(habits[0].name, 'Habit A')
        self.assertEqual(habits[1].name, 'Habit B')
