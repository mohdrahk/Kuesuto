from django.shortcuts import render
from django.http import HttpResponse
from .models import Plan, Task
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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

@login_required
def profile(request):
    return render(request, 'users/profile.html')


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