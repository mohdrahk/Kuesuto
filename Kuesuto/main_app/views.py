import os
from django.conf import settings
from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Plan, Task, Profile, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import PlanForm, TaskFormSet
from django.contrib.auth import login
from .forms import SignupForm

# @login_required

class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['avatar']
    template_name = 'main_app/profile.html'
    success_url = '/profile/'

    def get_object(self):
        return self.request.user.profile

class UserDelete(DeleteView):
    model = User
    template_name = 'main_app/profile_confirm_delete.html'
    success_url = '/'

    def get_object(self):
        return self.request.user



def profile(request):
    return render(request, 'main_app/profile.html')



class PlanCreate(CreateView):
    model = Plan
    form_class = PlanForm
    template_name = 'main_app/plan_form.html'

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



class PlanUpdate(UpdateView):
    model = Plan
    form_class = PlanForm
    template_name = 'main_app/plan_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['task_formset'] = TaskFormSet(
                self.request.POST,
                instance= self.object
            )
        else:
            context['task_formset'] = TaskFormSet(instance= self.object)
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



class PlanDelete(DeleteView):
    model = Plan
    success_url = '/plans/'

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def plans_index(request):
    plans = Plan.objects.all()
    return render(request, 'plans/index.html', {'plans': plans})

def plans_detail(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    return render(request, 'plans/detail.html', { 'plan':plan })




class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'duration', 'importance', 'color', 'notes', 'deadline']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'duration', 'importance', 'color', 'notes', 'deadline', 'position']

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/'

def signup(request):
    error_message = ''
    if request.method == 'POST':

        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get('avatar')

            profile, created = Profile.objects.get_or_create(user=user)
            if avatar:
                profile.avatar = avatar
                profile.save()

            login(request, user)
            return redirect('plans_index')
        else:
            error_message = 'Invalid sign up - try again'
    else:
        form = SignupForm()

    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
