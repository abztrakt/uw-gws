from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('uw_gws.views',
    url(r'groups/(?P<group>.*)/members/update/$', 'update_members', name='update_members'),
    url(r'groups/(?P<group>.*)/members/$', 'view_group_members', name='view_group_members'),
    url(r'groups/(?P<group>.*)/$', 'view_group_info', name='view_group_info'),
    url(r'groups/$', 'view_group_list', name='view_group_list'),
    url(r'^$','home_page',name='home_page'),
)
