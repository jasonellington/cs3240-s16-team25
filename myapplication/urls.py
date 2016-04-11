from django.conf.urls import patterns, url
from myapplication import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^register/$', views.register, name='register'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^manager/$', views.manager, name='admin'),
        url(r'^messaging/$', views.messaging, name='messaging'),
        url(r'^usergroup/$', views.user_to_group, name='addtogroup')
                       )