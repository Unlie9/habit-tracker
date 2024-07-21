from django.db.models import Q
from django.utils import timezone

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy

from habit_tracker.forms import CustomUserCreationForm, HabitForm, HabitSearchForm

from habit_tracker.models import (
    Habit,
    UserHabitDetail,
    UserHabit
)

from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
)


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    user_habits = UserHabit.objects.filter(user=user)
    user_habit_details = UserHabitDetail.objects.filter(user_habit__in=user_habits)
    num_user_habits = UserHabitDetail.objects.filter(user_habit__user=user).count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    paginator = Paginator(user_habit_details, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        "user": user,
        "user_habits": user_habits,
        "user_habit_details": user_habit_details,
        "num_user_habits": num_user_habits,
        "num_visits": num_visits + 1,
        "page": page,
    }

    return render(request, "habit_tracker/index.html", context=context)


# @login_required
# def my_habits(request):
#     if not request.user.is_authenticated:
#         return redirect('login')
#
#     user = request.user
#     user_habits = UserHabit.objects.filter(user=user)
#     user_habit_details = UserHabitDetail.objects.filter(user_habit__in=user_habits)
#
#     context = {
#         "user": user,
#         "user_habits": user_habits,
#         "user_habit_details": user_habit_details,
#     }
#
#     return render(request, "habit_tracker/my_habits.html", context=context)


class MyHabitsListView(LoginRequiredMixin, ListView):
    template_name = "habit_tracker/my_habits.html"
    context_object_name = "user_habits"
    paginate_by = 5

    def get_queryset(self):
        queryset = UserHabit.objects.filter(user=self.request.user).order_by("-date_of_assign")
        name_search = self.request.GET.get("name")
        if name_search:
            queryset = queryset.filter(name__icontains=name_search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MyHabitsListView, self).get_context_data(**kwargs)
        user_habits = context["user_habits"]
        user_habit_details = UserHabitDetail.objects.filter(user_habit__in=user_habits)
        num_user_habits = UserHabitDetail.objects.filter(user_habit__user=self.request.user).count()
        context["user_habit_details"] = user_habit_details
        context["num_user_habits"] = num_user_habits
        context["search_form"] = HabitSearchForm(self.request.GET)
        return context


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    context_object_name = "habits_list"
    template_name = "habit_tracker/all_habits.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Habit.objects.all().order_by("-id")
        name_search = self.request.GET.get('name', '')
        if name_search:
            queryset = queryset.filter(name__icontains=name_search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HabitListView, self).get_context_data(**kwargs)
        habits = context["habits_list"]
        num_habits = Habit.objects.count()
        context["habits"] = habits
        context["num_habits"] = num_habits
        context["search_form"] = HabitSearchForm(self.request.GET)
        return context


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
    success_url = reverse_lazy("my-habits")


@login_required
def assign_habit_to_user(request, pk):
    user = request.user
    habit = get_object_or_404(Habit, pk=pk)

    user_habit, created = UserHabit.objects.get_or_create(user=user, habit=habit)
    if created:
        user_habit.date_of_assign = timezone.now()
        user_habit.save()
        UserHabitDetail.objects.create(user_habit=user_habit)

    return redirect(reverse_lazy("all-habits"))


@login_required
def remove_habit_from_user(request, pk):
    user = request.user
    habit = get_object_or_404(Habit, pk=pk)

    user_habit = UserHabit.objects.filter(user=user, habit=habit).first()

    if user_habit:
        UserHabitDetail.objects.filter(user_habit=user_habit).delete()

    user_habits = UserHabit.objects.filter(user=user).order_by("-date_of_assign")
    paginator = Paginator(user_habits, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not page_obj and page_obj.has_previous():
        return redirect(f"{reverse_lazy("my-habits")}?page={page_obj.previous_page_number}")

    return redirect(reverse_lazy("my-habits"))


class UserHabitDetailUpdateView(LoginRequiredMixin, UpdateView):
    model = UserHabitDetail
    fields = ["days_to_achieve"]
    success_url = reverse_lazy("index")


class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


@login_required
def my_profile(request):
    user = request.user
    return render(request, "habit_tracker/my_profile.html", {"user": user})


@login_required
def confirm_operation(request, detail_id, operation):
    detail = get_object_or_404(UserHabitDetail, id=detail_id)

    context = {
        "detail": detail,
        "operation": operation
    }
    return render(request, "habit_tracker/confirmation_operation.html", context)


@login_required
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
