from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Member


@receiver(post_save, sender=Member)
def delete_duplicate_members(sender, instance, **kwargs):
    if instance.acceptance_status:
        Member.objects.filter(user=instance.user).exclude(pk=instance.pk).delete()
