from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group



# Create your models here.


class Message(models.Model):
    recipient = models.CharField(max_length=30)
    sender = models.CharField(max_length=30)
    message = models.TextField()
    encrypted = models.BooleanField(default=False)
    bites = models.BinaryField(null=True)
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.recipient


class Report(models.Model):
    author = models.ForeignKey(User, null=True)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=128)
    content = models.TextField()
    security = models.BooleanField(default=False)
    encrypted = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)
    users = models.ManyToManyField(User, related_name='permittedUsers')
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return self.description


class PublicKey(models.Model):
    user = models.CharField(max_length=30)
    Nval = models.TextField()
    Eval = models.TextField()


class ReportFile(models.Model):
    reporter = models.ForeignKey(Report)
    file = models.FileField()
    hash = models.CharField(max_length=40, default=None, null=True)

    def __str__(self):
        return self.file.name


class ReportFolder(models.Model):
    owner = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=50)
    reports = models.ManyToManyField(Report)

class ReportComment(models.Model):
    reporton = models.ForeignKey(Report)
    poster = models.ForeignKey(User)
    comment = models.TextField()


class UserNumber(models.Model):
    user = models.ForeignKey(User, unique=True)
    phone_number = models.CharField(max_length=13, null=True, default=None)

    def get_number(self):
        return self.phone_number

    def set_number(self, number):
        self.phone_number = number