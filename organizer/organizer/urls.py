from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'organizer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^organizer/', 'base.views.showMain', name='main'),
    url(r'^graph/','base.views.showD3_graph_test', name='showD3_graph_test'),
    url(r'^getGraph/','base.views.getGraph', name='getGraph'),
    url(r'^addLink/','base.views.addLink', name='addLink'),
    url(r'^removeLink/','base.views.removeLink', name='removeLink'),
    url(r'^addNode/','base.views.addNode', name='addNode'),
    url(r'^removeNode/','base.views.removeNode', name='removeNode'),
    url(r'^fixNodePos/','base.views.fixNodePos', name='fixNodePos'),
    url(r'^resetAllNodePos/','base.views.resetAllNodePos', name='resetAllNodePos'),
    url(r'^getNodeEditDiv/','base.views.getNodeEditDiv', name='getNodeEditDiv'),
    url(r'^saveNode/','base.views.saveNode', name='saveNode'),
)
