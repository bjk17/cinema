from django.conf.urls import include, url
from movies import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]
