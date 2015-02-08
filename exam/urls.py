try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from exam import views


urlpatterns = patterns('exam.views',
        url(r'^savetime', views.savetime, name='savetime'),
        url(r'^test/(?P<t_id>[-\w.]+)/$', views.test_name, name='test_name'),
        url(r'^test/(?P<t_id>[-\w.]+)/ques/$', views.test, name='test'),
        url(r'^$', views.index, name='index'),
        url(r'^result/test/(?P<t_id>[-\w.]+)/$', views.test_results, name='test_results'),
        url(r'^results/', views.results, name='results'),
        url(r'^tests/$', views.test_select, name='select_test'),




)
