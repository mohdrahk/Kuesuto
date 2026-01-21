from django.shortcuts import render
from django.http import HttpResponse
from .models import Plan

def home(request):
    return render(request, 'home.html'),

def about(request):
    return render(request, 'about.html'),

def plans_index(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'plans/index.html', {'plans': plans})

def plans_detail(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    return render(request, 'plans/detail.html', { 'plan':plan })
