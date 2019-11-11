from django.db import models
from django.contrib.auth.models import AbstractUser, User


class CustomUser(AbstractUser):
    USER_TYPE_CLIENT = 'client'
    USER_TYPE_BARBER = 'barber'
    USER_TYPES = ((USER_TYPE_CLIENT, 'client'), (USER_TYPE_BARBER, 'barber'))
    type = models.CharField(max_length=100, choices=USER_TYPES)
