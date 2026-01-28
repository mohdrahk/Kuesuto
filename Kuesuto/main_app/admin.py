from django.contrib import admin
from .models import Profile,Rank, Plan, Task

# Register your models here.

admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Plan)
admin.site.register(Task)
