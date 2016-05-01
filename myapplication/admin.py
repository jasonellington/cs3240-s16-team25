from django.contrib import admin
from myapplication.models import Message, Report, ReportFile

# Register your models here.


admin.site.register(Message)
admin.site.register(Report)
admin.site.register(ReportFile)