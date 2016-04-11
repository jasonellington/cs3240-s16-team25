from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Message(models.Model):
    recipient = models.CharField(max_length=30)
    sender = models.CharField(max_length=30)
    message = models.TextField()
    opened = models.BooleanField(default=False)

    def __str__(self):
        return self.recipient

class Report(models.Model):
    author = models.ForeignKey(User, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=128)
    content = models.TextField()
    security = models.BooleanField(default=False)