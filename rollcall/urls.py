from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from rollcall.groups.views import (
    GroupListView,
    GroupDetailView,
    GroupStatesView,
    GroupStateListView,
    GroupUpdate,
)
from rollcall.people.views import PersonListView, PersonDetailView



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rollcall.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(
        r'^people/$', 
            PersonListView.as_view(),
            name='person-list',
    ),
    url(
        r'^people/(?P<slug>.*)$',
            PersonDetailView.as_view(),
            name='person-detail',
    ),

    url(
        r'^group/$',
            GroupListView.as_view(),
            name='group-list',
    ),
    url(
        r'^group/(?P<slug>.*?)/state$',
        GroupUpdate.as_view(),
        name='group-state',
    ),
    url(
        r'^group/(?P<slug>.*)$',
            GroupDetailView.as_view(),
            name='group-detail',
    ),
    url(
        r'^group-state/$',
            GroupStatesView.as_view(),
            name='group-list-states',
    ),
    url(
        r'^group-state/(?P<state>.*)$',
            GroupStateListView.as_view(),
            name='group-list-by-state',
    ),
)
