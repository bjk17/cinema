from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^wm/', include('watchmen.urls')),
    url(r'^$', include('movies.urls')),
]
