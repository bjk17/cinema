from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^wm/', include('watchmen.urls')),
    url(r'^$', include('movies.urls')),
)
