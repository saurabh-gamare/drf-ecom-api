from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username


class Log(models.Model):
    endpoint = models.CharField(max_length=255, null=True)
    request = models.JSONField(null=True)
    headers = models.JSONField(null=True)
    response = models.JSONField(null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.endpoint
