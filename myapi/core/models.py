from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
#
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)


class Task(models.Model):
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='creator', null=False, default=1)
    executors = models.ManyToManyField(User)

    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=1000)
    task_end = models.DateField()
