from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import User


class BenefactorManager(models.Manager):
    def related_tasks_to_benefactor(self):
        return Task.objects.filter(assigned_benefactor=self)


class CharityManager(models.Model):
    def related_tasks_to_charity(self):
        return Task.objects.filter(charity=self)


class Benefactor(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    experience = models.SmallIntegerField(default=0, validators=[MaxValueValidator(2), MinValueValidator(0)])
    free_time_per_week = models.PositiveSmallIntegerField(default=0)

    object = BenefactorManager()

    def __str__(self):
        return self.user.get_full_name()


class Charity(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)

    object = CharityManager()

    def __str__(self):
        return self.name


class Task(models.Model):
    GENDER = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    STATE = (
        ('P', 'Pending'),
        ('W', 'Waiting'),
        ('A', 'Assigned'),
        ('D', 'Done')
    )
    assigned_benefactor = models.ForeignKey(Benefactor, on_delete=models.SET_NULL, null=True)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    age_limit_from = models.IntegerField(blank=True, null=True)
    age_limit_to = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE, default='P')
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title
