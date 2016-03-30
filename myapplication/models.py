from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
