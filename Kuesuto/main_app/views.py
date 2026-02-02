import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
import json
from .services.ai_service import GeminiAIService
from django.http import JsonResponse
from .models import Plan, Task, Profile, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import PlanForm, TaskFormSet
from django.contrib.auth import login
from .forms import SignupForm
from django.contrib import messages

# @login_required


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ["avatar"]
    template_name = "main_app/profile.html"
    success_url = "/profile/"

    def get_object(self):
        return self.request.user.profile


class UserDelete(DeleteView):
    model = User
    template_name = "main_app/profile_confirm_delete.html"
    success_url = "/"

    def get_object(self):
        return self.request.user


def profile(request):
    return render(request, "main_app/profile.html")


class PlanCreate(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = PlanForm
    template_name = "main_app/plan_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["task_formset"] = TaskFormSet(self.request.POST)
        else:
            context["task_formset"] = TaskFormSet()
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        task_formset = context["task_formset"]

        if not task_formset.is_valid():
            return self.form_invalid(form)

        plan = form.save(commit=False)
        plan.user = self.request.user
        plan.save()

        task_formset.instance = plan
        tasks = task_formset.save(commit=False)

        for i, task in enumerate(tasks, start=1):
            task.plan = plan
            task.position = i
            task.save()

        self.object = plan
        return super().form_valid(form)



class PlanUpdate(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = "main_app/plan_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context["task_formset"] = TaskFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["task_formset"] = TaskFormSet(instance=self.object)
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        task_formset = context["task_formset"]

        if not task_formset.is_valid():
            return self.form_invalid(form)

        plan = form.save()
        tasks = task_formset.save(commit=False)

        for i, task in enumerate(tasks, start=1):
            task.plan = plan
            task.position = i
            task.save()

        self.object = plan
        return super().form_valid(form)



class PlanDelete(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = "/plans/"


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def plans_index(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, "plans/index.html", {"plans": plans})


def plans_detail(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    return render(request, "plans/detail.html", {"plan": plan})


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["name", "duration", "importance", "color", "notes", "deadline"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = [
        "name",
        "duration",
        "importance",
        "color",
        "notes",
        "deadline",
        "position",
    ]






class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = "/"


@login_required
def task_toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.is_completed = not task.is_completed
    task.save()

    profile = request.user.profile
    all_tasks = task.plan.task_set.all()

    if task.is_completed:
        profile.score +=10


        if all_tasks.filter(is_completed=True).count() == all_tasks.count():
            profile.score += 30
            messages.success(request, f'🎉 +10 points! +30 Bonus for completing all tasks! Total: {profile.score}')
        else:
            messages.success(request, f'✅ +10 points! Total: {profile.score}')
        profile.save()


    return redirect('plans_detail', plan_id=task.plan.id)

def signup(request):
    error_message = ""
    if request.method == "POST":

        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get("avatar")

            profile, created = Profile.objects.get_or_create(user=user)
            if avatar:
                profile.avatar = avatar
                profile.save()

            login(request, user)
            return redirect("plans_index")
        else:
            error_message = "Invalid sign up - try again"
    else:
        form = SignupForm()

    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


# @login_required
# @require_http_methods(["POST"])
def ask_ai(request):
    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()

        if not question:
            return JsonResponse(
                {"success": False, "error": "Please ask a question"}, status=400
            )

        profile = request.user.profile

        # Get all plans FIRST (don't slice!)
        all_plans = Plan.objects.filter(user=request.user)
        all_tasks = Task.objects.filter(plan__user=request.user)

        # Count active plans from ALL plans
        active_plans_count = all_plans.filter(is_completed=False).count()
        active_tasks_count = all_tasks.filter(is_completed=False).count()

        # NOW get only 5 plans for the data
        recent_plans = all_plans[:5]
        plans_data = [
            {"name": p.name, "completed": p.is_completed} for p in recent_plans
        ]

        user_data = {
            "username": request.user.username,
            "score": profile.score,
            "rank": profile.current_rank,
            "active_plans": active_plans_count,
            "active_tasks": active_tasks_count,
            "completed_tasks": Task.objects.filter(
                plan__user=request.user, is_completed=True
            ).count(),
            "plans": plans_data,
        }

        ai_service = GeminiAIService()
        answer = ai_service.answer_question(question, user_data)

        return JsonResponse({"success": True, "answer": answer})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
