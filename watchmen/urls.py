from django.conf.urls import include, url
from watchmen import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^id/', views.id, name='id'),
    url(r'^add/', views.add, name='add'),
    url(r'^remove/', views.remove, name='remove'),
]
