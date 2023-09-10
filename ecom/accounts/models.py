from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
