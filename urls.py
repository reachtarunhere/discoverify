from django.conf.urls import patterns, url
from discoverify.views import *

urlpatterns = patterns('',
		url(r'^addpath/$', create_path, name='create path'),
        url(r'^editpath/(?P<path_id>\d+)/$',edit_path_view,name='editing paths'),
        url(r'^updatepath/$',update_path,name='real ajax calls here :p'),
        url(r'^getsteps/$',get_steps,name='get ajax for all steps of a path'),
        url(r'^stepend/$',add_step_end,name='add step in the end'),
        url(r'^updatestep/(?P<step_id>\d+)/$',update_step,name='url for both updating steps and getting info'),
        url(r'^path/(?P<path_id>\d+)/$',path_details_view,name='individual path learning page'),
        url(r'^register/$',InitialRegistrationView,name='register for creators'),
        url(r'^login/$',user_login,name='main login'),
        url(r'^profile/$',profile,name='main login'),
        url(r'^logmeout/$',logout_view,name='main login'),
        url(r'^$',home_view,name='landing page'),
        url(r'^createwizard/$',create_dummy_view,name='create_dummy_view')
		)
