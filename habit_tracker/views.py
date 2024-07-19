from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from habit_tracker.forms import CustomUserCreationForm, HabitForm
from habit_tracker.models import (
    Habit,
    User,
    UserHabitDetail,
    UserHabit
)
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    CreateView,
    DeleteView,
    FormView
)


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    user_habits = UserHabit.objects.filter(user=user)
    user_habit_details = UserHabitDetail.objects.filter(user_habit__in=user_habits)
    num_user_habits = UserHabit.objects.count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "user": user,
        "user_habits": user_habits,
        "user_habit_details": user_habit_details,
        "num_user_habits": num_user_habits,
        "num_visits": num_visits + 1,
    }

    return render(request, "habit_tracker/index.html", context=context)


class HabitsListView(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits_list"
    template_name = "habit_tracker/all-habits.html"
    paginate_by = 5

    # def get_context_data(self, object_list=None, **kwargs):
    #     context = super(ManufacturerListView, self).get_context_data(**kwargs)
    #
    #     context["search_form"] = ManufacturerNameSearchForm()
    #     return context
    #
    # def get_queryset(self):
    #     queryset = Car.objects.all()
    #     name = self.request.GET.get("name")
    #
    #     if name:
    #         return queryset.filter(model__icontains=name)
    #     return queryset


@login_required()
def my_profile(request):
    user = request.user
    return render(request, "habit_tracker/my_profile.html", {"user": user})


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    paginate_by = 10


class HabitDetailView(LoginRequiredMixin, DetailView):
    model = Habit


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    success_url = ""


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    success_url = ""


class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    success_url = reverse_lazy("")


class HabitAssignView(LoginRequiredMixin, FormView):
    form_class = HabitForm
