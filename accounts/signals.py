from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfiles, UserAddress

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfiles.objects.create(user=instance,
                                    )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofiles.save()
