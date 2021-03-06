from django.conf.urls import patterns, url
from myapplication import views
from django.contrib.auth import views as v

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^register/$', views.register, name='register'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^manager/$', views.manager, name='admin'),
        url(r'^messaging/$', views.messaging, name='messaging'),
        url(r'^settings/$', views.settings, name = 'settings'),
        url(r'^usergroup/$', views.user_to_group, name='addtogroup'),
        url(r'^makemanager/$', views.make_manager, name='makemanager'),
        url(r'^reports/$', views.reports, name='reports'),
        url(r'^makereport/$', views.new_report, name='makemanager'),
        url(r'^editreport/$', views.edit_report, name='editreport'),
        url(r'^viewreport/$', views.view_report, name='viewreport'),
        url(r'^makefolder/$', views.new_folder, name='newfolder'),
        url(r'^addtofolder/$', views.edit_folder, name='addtofolder'),
        url(r'^viewfolder/$', views.view_folder, name='viewfolder'),
        url(r'^fdalogin/$', views.fda_login, name='fdalogin'),
        url(r'^fdalistreports/$', views.fda_list_reports, name='fdalistreports'),
        url(r'^fdagetreport/$', views.fda_get_report, name='fdagetreport'),
        url(r'^userreport/$', views.user_to_report, name='usertoreport'),
        url(r'^deletefolder/$', views.delete_folder, name='deletefolder'),
        url(r'^groupreport/$', views.group_to_report, name='grouptoreport'),
        url(r'^groups/$', views.groups, name='groups'),

                       )