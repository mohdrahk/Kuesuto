from django.contrib import admin
from .models import Profile, Plan, Task , Rank

# Register your models here.

admin.site.register(Profile)
admin.site.register(Rank)
admin.site.register(Plan)
admin.site.register(Task)
