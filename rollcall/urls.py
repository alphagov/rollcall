from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

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
)
