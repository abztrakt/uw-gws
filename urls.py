from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('uw_gws.views',
    url(r'groups/(?P<group>\w+)/$', 'view_group_info', name='view_group_info'),
)
