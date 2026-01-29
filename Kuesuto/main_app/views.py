from django.shortcuts import render
from django.http import HttpResponse
from .models import Plan, Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import PlanForm, TaskFormSet

# @login_required

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

        for obj in task_formset.deleted_objects:
            obj.delete()

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

        for objc in task_formset.deleted_objects:
            objc.delete()

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
    plans = Plan.objects.filter(user=request.user)
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
