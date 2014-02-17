from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from foodtrucks.views import display_page

urlpatterns = patterns('',
    url(r'^$', display_page),
)
