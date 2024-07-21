from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from habit_tracker.forms import CustomUserCreationForm, HabitForm, DeleteHabitForm
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


@login_required
def my_habits(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    user_habits = UserHabit.objects.filter(user=user)
    user_habit_details = UserHabitDetail.objects.filter(user_habit__in=user_habits)

    context = {
        "user": user,
        "user_habits": user_habits,
        "user_habit_details": user_habit_details,
    }

    return render(request, "habit_tracker/my_habits.html", context=context)


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits_list"
    template_name = "habit_tracker/all_habits.html"
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


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    success_url = reverse_lazy("all-habits")

    def form_valid(self, form):
        habit = form.save()
        UserHabit.objects.create(user=self.request.user, habit=habit)
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = "habit_tracker/habit_form.html"
    success_url = reverse_lazy("all-habits")

    def get_queryset(self):
        return Habit.objects.filter(userhabit__user=self.request.user)


class HabitDeleteView(LoginRequiredMixin, DeleteView):
    model = Habit
    form_class = DeleteHabitForm
    template_name = "habit_tracker/habit_confirm_delete.html"
    success_url = reverse_lazy("all-habits")

    def get_queryset(self):
        return Habit.objects.filter(userhabit__user=self.request.user)


class AssignHabitView(LoginRequiredMixin, FormView):
    model = Habit
    form_class = HabitForm
    template_name = "habit_tracker/assign_habit.html"

    def form_valid(self, form):
        habit = form.cleaned_data['habit']
        user = self.request.user
        user_habit, created = UserHabit.objects.get_or_create(user=user, habit=habit)

        if created:
            UserHabitDetail.objects.create(user_habit=user_habit)
        return redirect("all-habits")


class UserHabitDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = UserHabitDetail
    fields = "__all__"
    success_url = reverse_lazy("my-habits")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     return super().form_valid(form)

# def register_view(request):
#     if request.method == "POST":
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("all-habits")
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, "registration/register.html", {"form": form})


@login_required
def my_profile(request):
    user = request.user
    return render(request, "habit_tracker/my_profile.html", {"user": user})


def confirm_operation(request, detail_id, operation):
    detail = get_object_or_404(UserHabitDetail, id=detail_id)

    context = {
        "detail": detail,
        "operation": operation
    }
    return render(request, "habit_tracker/confirmation_operation.html", context)


def complete_operation(request, detail_id, operation):
    detail = get_object_or_404(UserHabitDetail, id=detail_id)

    if detail.user_habit.user == request.user:
        if operation == "completed":
            detail.days_to_achieve -= 1
            detail.skip_day = False
        elif operation == "not completed":
            detail.skip_day = True
        elif operation == "reset":
            detail.days_to_achieve = 21
            detail.skip_day = False

    detail.save()
    return redirect("index")
