from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from foodtrucks.views import display_page, show_diagrams

urlpatterns = patterns('',
    url(r'^$', display_page),
    url(r'^(?P<diagram>\w+)/$', show_diagrams),
)
