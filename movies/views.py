#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

import urllib2
import json

import sys

# Create your views here.
def index(request):
    return HttpResponse("<h1>Hallo heimur!</h1> <p>Thetta er prufusidan okkar.</p>")

def requestMovies(request):

    url = 'http://apis.is/cinema'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
        
    theater = data['results'][4]['showtimes'][0]['theater']
    

    for movie in data['results']:
        print movie['title']
        print movie['released']
        print movie['restricted']
        print movie['imdb']
        print movie['image']
        for cinema in movie['showtimes']:
            print cinema['theater']
            for time in cinema['schedule']:
                print time


    return HttpResponse("<h1>Hallo heimur!</h1> <p> %s </p>" % theater)


 
'''
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache (for next time)
    return the generated page
'''