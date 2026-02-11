from django.forms import ModelForm
from django import forms
from .models import Plan, Task
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar']




class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'duration', 'color']

# this connects multiple tasks to one plan, also for creating/editing tasks on the same page as plan
TaskFormSet = inlineformset_factory(
    Plan,
    Task,
    fields=['name', 'duration', 'importance', 'color', 'notes'],
    extra=1,
)
