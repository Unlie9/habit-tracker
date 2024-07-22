from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from habit_tracker.models import Habit, UserHabit, UserHabitDetail
from habit_tracker.forms import CustomUserCreationForm, HabitForm, HabitSearchForm

User = get_user_model()


class HabitTrackerViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.habit = Habit.objects.create(name='Test Habit', description='Test Description')

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/index.html')

    def test_my_habits_view(self):
        response = self.client.get(reverse('my-habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/my_habits.html')

    def test_all_habits_view(self):
        response = self.client.get(reverse('all-habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/all_habits.html')

    def test_assign_habit_to_user(self):
        response = self.client.post(reverse('assign-habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserHabit.objects.filter(user=self.user, habit=self.habit).exists())

    def test_remove_habit_from_user(self):
        user_habit = UserHabit.objects.create(user=self.user, habit=self.habit)
        response = self.client.post(reverse('remove-habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserHabit.objects.filter(user=self.user, habit=self.habit).exists())

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_my_profile_view(self):
        response = self.client.get(reverse('my-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habit_tracker/my_profile.html')

    def test_my_habits_view_pagination(self):
        for _ in range(10):
            habit = Habit.objects.create(name=f'Habit {_}', description=f'Description {_}')
            UserHabit.objects.create(user=self.user, habit=habit)
        response = self.client.get(reverse('my-habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])

    def test_all_habits_view_pagination(self):
        for _ in range(10):
            Habit.objects.create(name=f'Habit {_}', description=f'Description {_}')
        response = self.client.get(reverse('all-habits'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['is_paginated'])

    def test_search_habits_in_all_habits_view(self):
        Habit.objects.create(name='Searchable Habit', description='Searchable Description')
        response = self.client.get(reverse('all-habits') + '?name=Searchable')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Searchable Habit')

    def test_my_profile_view_contains_user(self):
        response = self.client.get(reverse('my-profile'))
        self.assertContains(response, self.user.username)
