from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from habit_tracker.models import UserHabitDetail, Habit, UserHabit
from habit_tracker.forms import HabitSearchForm

User = get_user_model()
client = Client()


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = client
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.habit1 = Habit.objects.create(name='Exercise', description='Morning exercise')
        self.habit2 = Habit.objects.create(name='Reading', description='Read a book')
        self.user_habit1 = UserHabit.objects.create(user=self.user, habit=self.habit1)
        self.user_habit2 = UserHabit.objects.create(user=self.user, habit=self.habit2)
        self.user_habit_detail1 = UserHabitDetail.objects.create(user_habit=self.user_habit1, days_to_achieve=21)
        self.user_habit_detail2 = UserHabitDetail.objects.create(user_habit=self.user_habit2, days_to_achieve=15)
        self.client.login(username='testuser', password='testpass')

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'habit_tracker/index.html')

    def test_index_view_context(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('user_habits', response.context)
        self.assertIn('num_user_habits', response.context)
        self.assertIn('num_visits', response.context)
        self.assertIn('search_form', response.context)
        self.assertIn('user_habit_details', response.context)

    def test_index_view_search(self):
        response = self.client.get(reverse('index'), {'name': 'Exercise'})
        self.assertContains(response, 'Exercise')
        self.assertNotContains(response, 'Reading')

    def test_index_view_num_visits(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(self.client.session['num_visits'], 1)
        response = self.client.get(reverse('index'))
        self.assertEqual(self.client.session['num_visits'], 2)

    def test_index_view_invalid_search_form(self):
        response = self.client.get(reverse('index'), {'name': 'x' * 101})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_habit_details'].count(), 2)

    def test_index_view_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("index")}')


class MyHabitsListViewTests(TestCase):
    def setUp(self):
        self.client = client
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.habit1 = Habit.objects.create(name='Exercise', description='Morning exercise')
        self.habit2 = Habit.objects.create(name='Reading', description='Read a book')
        self.user_habit1 = UserHabit.objects.create(user=self.user, habit=self.habit1)
        self.user_habit2 = UserHabit.objects.create(user=self.user, habit=self.habit2)
        self.user_habit_detail1 = UserHabitDetail.objects.create(user_habit=self.user_habit1, days_to_achieve=21)
        self.user_habit_detail2 = UserHabitDetail.objects.create(user_habit=self.user_habit2, days_to_achieve=15)
        self.client.login(username='testuser', password='testpass')

    def test_my_habits_list_view_status_code(self):
        response = self.client.get(reverse('my-habits'))
        self.assertEqual(response.status_code, 200)

    def test_my_habits_list_view_template(self):
        response = self.client.get(reverse('my-habits'))
        self.assertTemplateUsed(response, 'habit_tracker/my_habits.html')

    def test_my_habits_list_view_context(self):
        response = self.client.get(reverse('my-habits'))
        self.assertEqual(response.context['user'], self.user)
        self.assertIn('user_habits', response.context)
        self.assertIn('num_user_habits', response.context)
        self.assertIn('search_form', response.context)
        self.assertIn('user_habit_details', response.context)

    def test_my_habits_list_view_pagination(self):
        for i in range(5):
            habit = Habit.objects.create(name=f'Habit{i}', description=f'Description{i}')
            UserHabit.objects.create(user=self.user, habit=habit)

        response = self.client.get(reverse('my-habits'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['user_habits']), 4)

    def test_my_habits_list_view_search(self):
        response = self.client.get(reverse('my-habits'), {'name': 'Exercise'})
        self.assertContains(response, 'Exercise')
        self.assertNotContains(response, 'Reading')

    def test_my_habits_list_view_invalid_search_form(self):
        response = self.client.get(reverse('my-habits'), {'name': 'x' * 101})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user_habit_details'].count(), 2)

    def test_my_habits_list_view_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('my-habits'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("my-habits")}')


class HabitListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.habit1 = Habit.objects.create(name='Exercise', description='Morning exercise')
        self.habit2 = Habit.objects.create(name='Reading', description='Read a book')
        self.habit3 = Habit.objects.create(name='Meditation', description='Daily meditation')
        self.user_habit = UserHabit.objects.create(user=self.user, habit=self.habit1)
        self.client.login(username='testuser', password='testpass')

    def test_habit_list_view_status_code(self):
        response = self.client.get(reverse('all-habits'))
        self.assertEqual(response.status_code, 200)

    def test_habit_list_view_template(self):
        response = self.client.get(reverse('all-habits'))
        self.assertTemplateUsed(response, 'habit_tracker/all_habits.html')

    def test_habit_list_view_context(self):
        response = self.client.get(reverse('all-habits'))
        self.assertIn('habits_list', response.context)
        self.assertIn('user_habits', response.context)
        self.assertIn('num_habits', response.context)
        self.assertIn('search_form', response.context)

    def test_habit_list_view_pagination(self):
        for i in range(5):
            Habit.objects.create(name=f'Habit{i}', description=f'Description{i}')

        response = self.client.get(reverse('all-habits'))
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['habits_list']), 4)

    def test_habit_list_view_search(self):
        response = self.client.get(reverse('all-habits'), {'name': 'Reading'})
        self.assertContains(response, 'Reading')
        self.assertNotContains(response, 'Exercise')
        self.assertNotContains(response, 'Meditation')

    def test_habit_list_view_without_login(self):
        self.client.logout()
        response = self.client.get(reverse('all-habits'))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("all-habits")}')

