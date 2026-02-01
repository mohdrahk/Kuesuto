from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    #profile CRUD
    path('profile/', views.ProfileUpdate.as_view(), name='users_profile'),
    path('profile/delete/', views.UserDelete.as_view(), name='profile_delete'),

    path('accounts/signup/', views.signup, name='signup'),


    # plans CRUD
    path('plans/',views.plans_index, name='plans_index'),
    path('plans/<int:plan_id>/', views.plans_detail, name='plans_detail'),

    path('plans/create/', views.PlanCreate.as_view(), name='plans_create'),
    path('plans/<int:pk>/edit/', views.PlanUpdate.as_view(), name='plans_update'),
    path('plans/<int:pk>/delete/', views.PlanDelete.as_view(), name='plans_delete'),
    path('ai/ask/', views.ask_ai, name='ask_ai'),


    # tasks CRUD
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='tasks_detail'),
    path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name='tasks_delete'),
    path('tasks/<int:task_id>/toggle/', views.task_toggle_complete, name='task_toggle_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

