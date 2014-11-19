#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

from movies.models import Movie,Showtime,Timestamp

import urllib2, json, sys, time


# Create your views here.
def index(request):
    return HttpResponse("<h1>Hallo heimur!</h1> <p>Thetta er prufusidan okkar.</p>")

def requestMovies(request):

    url = 'http://apis.is/cinema'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
        
    theater = data['results'][4]['showtimes'][0]['theater']

    # Get time last request was made and current time
    lastRequest = Timestamp.objects.values('timeFetched')
    currentTime = time.time()
    lastTime = lastRequest[0]['timeFetched']
    #print currentTime - lastTime
    
    # If there were less than x mins since
    # last request we wont make another request
    # Else we will
    if((currentTime-lastTime)>30):
        updateDatabase(data['results'])
        print "Ég sótti gögn"  
    else:
        print "Nýbúið að sækja gögn"  

    return HttpResponse("<h1>Hallo heimur!</h1> <p> %s </p>" % theater)

def updateDatabase(data):
    # Delete old movie-entries from db
    Showtime.objects.all().delete()
    Movie.objects.all().delete()

    # Insert newly fetched movies into db
    for movie in data:
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
    
    newTimestamp()

def newTimestamp():
    # Delete old timestamp from db
    Timestamp.objects.all().delete()

    # Get current time
    ts = time.time()

    # Save current time in db
    t = Timestamp(timeFetched=ts)
    t.save()


        #We need to "update" the database, check if movie is in newly fetched films
        #If it is
        #if not we remove the film 

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
 
'''
given a URL, try finding that page in the cache
if the page is in the cache:
    return the cached page
else:
    generate the page
    save the generated page in the cache (for next time)
    return the generated page
'''