from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    team = models.CharField(max_length=40, null=True)
