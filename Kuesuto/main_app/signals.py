from django.db.models.signals import post_save, pre_save
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
