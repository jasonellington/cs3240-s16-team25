
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import django
django.setup()

from django.contrib.auth.models import User


def populate():

    if len(list(User.objects.filter(username = "manager").all())) == 0:
        add_manager()
    pass

def add_manager():
    u = User.objects.create(username="manager", is_staff= True)
    u.set_password("password")
    u.save()



if __name__ == '__main__':
    populate()