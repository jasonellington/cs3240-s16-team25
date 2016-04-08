from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Message(models.Model):
    recipient = models.CharField(max_length=30)
    sender = models.CharField(max_length=30)
    message = models.TextField()
    opened = models.BooleanField(default=False)
