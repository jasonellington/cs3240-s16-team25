from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.models import User

from mysite import settings
from django.conf.urls.static import static
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken import views

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^myapplication/', include('myapplication.urls')),
                       url(r'^gettoken/', views.obtain_auth_token),
                       url(r'^api-auth/', include('rest_framework.urls'), name='rest_framework'),
                       ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
