from django.forms import ModelForm
from .models import Plan, Task
from django.forms import inlineformset_factory

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'duration', 'color']

TaskFormSet = inlineformset_factory(
    Plan,
    Task,
    fields=['name', 'duration', 'importance', 'color', 'notes'],
    extra=1,
    can_delete=True
)
