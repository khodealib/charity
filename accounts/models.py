from django.contrib.auth.models import AbstractUser
from django.db import models

from charities.models import Task


class UserManager(models.Manager):
    def all_related_tasks_to_user(self):
        return Task.objects.filter(
            status='P',
            charity__user=self,
            assigned_benefactor__user=self
        )


class User(AbstractUser):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    address = models.TextField(blank=True, null=True)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    objects = UserManager()
