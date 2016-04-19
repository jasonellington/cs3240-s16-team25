from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^myapplication/', include('myapplication.urls')),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
