
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.contrib.auth.models import User
from myapplication.models import UserProfile


def populate():

    if len(list(UserProfile.objects.filter(user__username="manager").all())) == 0:
        add_manager()


def add_manager():
    u = User.objects.create(username="manager", password="password")
    u.save()
    m = UserProfile.objects.create(user=u,admin=True)

    m.save()


if __name__ == '__main__':
    populate()