from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',

                       url(r'^exam/', include('exam.urls', namespace="exam")),
                       url(r'^', include('exam.urls', namespace="exam")),
                       url(r'^user/', include('user.urls', namespace="user")),
                       # Examples:
                       # url(r'^$', 'Exam_Portal.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
         'serve',
         {'document_root': settings.MEDIA_ROOT}), )
if settings.DEBUG:
    urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)