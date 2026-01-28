from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="main_app/static/profile_images/",  default= "")
    score = models.IntegerField(default=0)
    current_rank = models.ForeignKey(
        "Rank", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.user.username


class Rank(models.Model):
    name = models.CharField(max_length=50)
    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField()
    icon = models.ImageField(upload_to="main_app/static/profile_images/", default="")
    order_position = models.IntegerField()

    def __str__(self):
        return self.name


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


class Task(models.Model):
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    importance = models.BooleanField(default=False)
    color = models.CharField(max_length=7)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    position = models.IntegerField()
    deadline = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
