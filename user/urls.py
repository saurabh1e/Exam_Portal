from django.conf.urls import patterns, url
from exam import views
from user import views

urlpatterns = patterns('',
                       url(r'^profile/(?P<p_id>\w+)$', views.user_profile, name='user_profile'),
                       url(r'^register/$', views.register_user, name='register'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^profile/$', views.curr_profile, name='curr_profile'),
                       url(r'^all/$', views.All_User, name='user_all'),
                       url(r'^data/$', views.user_data, name='user_data'),

)

