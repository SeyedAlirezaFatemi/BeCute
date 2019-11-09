from django.db import models
from django.contrib.auth.models import AbstractUser, User


class CustomUser(AbstractUser):
    type = models.CharField(max_length=100, choices=(('client', 'client'), ('barber', 'barber')))
