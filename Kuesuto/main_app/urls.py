from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # plans CRUD
    path('plans/',views.plans_index, name='plans_index'),
    path('plans/<int:plan_id>/', views.plans_detail, name='plans_detail'),
    path('profile/', views.profile_view, name='users-profile'),
    path('plans/create/', views.PlanCreate.as_view(), name='plans_create'),
    path('plans/<int:pk>/edit/', views.PlanUpdate.as_view(), name='plans_update'),
    path('plans/<int:pk>/delete/', views.PlanDelete.as_view(), name='plans_delete'),
]

