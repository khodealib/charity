from django.contrib.auth.models import AbstractUser
from django.db import models

from charities.models import Task


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

    def all_related_tasks_to_user(self):
        return Task.objects.all_related_tasks_to_user(self)
