from django.conf.urls import patterns, include, url
from movies import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Vefforritun.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
                       
    #prufa fyrir curl
    url(r'^request/', views.requestMovies, name='req'),
)
