from django.contrib import admin

# Register your models here.
from myapplication.models import UserProfile

admin.site.register(UserProfile)
