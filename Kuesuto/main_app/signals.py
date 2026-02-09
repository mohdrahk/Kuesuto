from django.db.models.signals import post_save, pre_save, post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone

from .models import Profile, Task, Rank


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Task)
def track_task_completion(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_task = Task.objects.get(pk=instance.pk)
            if not old_task.is_completed and instance.is_completed:
                profile = instance.plan.user.profile
                profile.score +=10

                plan = instance.plan
                all_tasks = plan.task_set.all()

                if all_tasks.filter(is_completed=True).count() == all_tasks.count():
                    tasks_with_deadline = all_tasks.exclude(deadline__isnull=True)
                    if tasks_with_deadline.exists():
                        all_on_time = all(t.updated_at.date() <= t.deadline for t in tasks_with_deadline if t.deadline)
                        if all_on_time:
                            profile.score += 30
                    plan.is_completed = True
                    plan.completed_at = timezone.now()
                    plan.save()

                rank = Rank.objects.filter(min_score__lte=profile.score, max_score__gte=profile.score).first()
                if rank:
                    profile.current_rank = rank
                profile.save()
        except Task.DoesNotExist:
            pass

@receiver(post_migrate)
def create_default_ranks(sender, **kwargs):
    if sender.name == 'main_app':
        ranks = [
            {'name': 'Bronze', 'min_score': 0, 'max_score': 99, 'order_position': 1, 'icon': 'rank/bronze.jpg'},
            {'name': 'Silver', 'min_score': 100, 'max_score': 299, 'order_position': 2, 'icon': 'rank/silver.jpg'},
            {'name': 'Gold', 'min_score': 300, 'max_score': 599, 'order_position': 3, 'icon': 'rank/gold.jpg'},
            {'name': 'Platinum', 'min_score': 600, 'max_score': 999, 'order_position': 4, 'icon': 'rank/platinum.jpg'},
            {'name': 'Emeralds', 'min_score': 1000, 'max_score': 1999, 'order_position': 5, 'icon': 'rank/emeralds.jpg'},
            {'name': 'Diamond', 'min_score': 2000, 'max_score': 999999, 'order_position': 6, 'icon': 'rank/diamond.jpg'},
        ]

