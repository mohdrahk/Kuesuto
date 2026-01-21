from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    duration = models.CharField(max_length=25)
    color = models.CharField(max_length=8)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plans_detail", kwargs={"plan_id": self.id})


