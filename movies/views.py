#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from movies.models import Movie,Showtime

import urllib2, json, sys


# Create your views here.
def index(request):
    return HttpResponse("<h1>Hallo heimur!</h1> <p>Thetta er prufusidan okkar.</p>")

def requestMovies(request):

    url = 'http://apis.is/cinema'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
        
    theater = data['results'][4]['showtimes'][0]['theater']

    saveToDatabase(data['results'])    

    '''for movie in data['results']:
        print movie['title']
        print movie['released']
        print movie['restricted']
        print movie['imdb']
        print movie['image']
        for cinema in movie['showtimes']:
            print cinema['theater']
            for time in cinema['schedule']:
                print time'''


    return HttpResponse("<h1>Hallo heimur!</h1> <p> %s </p>" % theater)

def saveToDatabase(data):
    for movie in data:
        #print int(unicode(movie['released']))
        indexOfYear = movie['released'].find(u"ára")
        m = Movie(title=movie['title'],
                    released=int(movie['released']), 
                    restricted=int(movie['released'][0:indexOfYear]), 
                    imdb=movie['imdb'], 
                    image=movie['image'])
        m.save()
        for cinema in movie['showtimes']:
            for time in cinema['schedule']:
                s = Showtime(movie=m, cinema=cinema['theater'], time=time)
                s.save()

 
'''
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache (for next time)
    return the generated page
'''