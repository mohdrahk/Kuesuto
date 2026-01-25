from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('plans/',views.plans_index, name='plans_index'),
    path('plans/<int:plan_id>/', views.plans_detail, name='plans_detail'),
    path('profile/', views.profile, name='users-profile'),
]

