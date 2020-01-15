from django.db import models
from django.contrib.auth.models import AbstractUser, User


class CustomUser(AbstractUser):
    USER_TYPE_CLIENT = "client"
    USER_TYPE_BARBER = "barber"
    USER_TYPES = ((USER_TYPE_CLIENT, "client"), (USER_TYPE_BARBER, "barber"))

    HAIR_TYPE_STRAIGHT = "Straight"
    HAIR_TYPE_CURLY = "Curly"
    HAIR_TYPE_WAVY = "Wavy"
    HAIR_TYPE_KINKY = "Kinky"
    HAIR_TYPES = ((HAIR_TYPE_WAVY, "Wavy"), (HAIR_TYPE_STRAIGHT, "Straight"), (HAIR_TYPE_CURLY, "Curly"), (HAIR_TYPE_KINKY, "Kinky"))

    type = models.CharField(max_length=100, choices=USER_TYPES)
    age = models.IntegerField(default=0, blank=True, null=True)
    about_me = models.CharField(max_length=500, default="", blank=True, null=True)
    residence_city = models.CharField(max_length=100, default="", blank=True, null=True)
    phone_customer = models.IntegerField(default=0, blank=True, null=True)
    hair_type = models.CharField(max_length=100, choices=HAIR_TYPES, default=HAIR_TYPE_STRAIGHT, blank=True, null=True)

    GENDER_TYPE_FEMALE = "F"
    GENDER_TYPE_MALE = "M"
    GENDER_TYPES = ((GENDER_TYPE_MALE, "M"), (GENDER_TYPE_FEMALE, "F"))
    gender = models.CharField(max_length=1, choices=GENDER_TYPES, default=GENDER_TYPE_FEMALE, blank=True, null=True)
