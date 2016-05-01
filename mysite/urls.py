from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User

from mysite import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
                       url(r'^myapplication/', include('myapplication.urls')),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
