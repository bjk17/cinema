#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from movies.models import Movie,Showtime,Timestamp

import urllib2, json, sys, time


# Create your views here.
def index(request):
    # return render_to_response('index.html', {})
    requestMovies(request)
    getMoviesFromDB(request)
    showMovies()
    return HttpResponse("<h1>Hallo heimur!</h1> <p>Thetta er prufusidan okkar.</p>")

def requestMovies(request):   
    # Get time last request was made and current time
    lastRequest = Timestamp.objects.values('timeFetched')
    currentTime = time.time()
    lastTime = 0
    
    if len(lastRequest)>0:
        lastTime = lastRequest[0]['timeFetched']
    
    # If there were less than 30 seconds since
    # the last request we wont make another request
    # Else we will
    if (currentTime-lastTime)>30:
        updateDatabase(request)
        print "Ég sótti gögn"  
    else:
        print "Nýbúið að sækja gögn"  

    return HttpResponse("<h1>Hallo heimur!</h1>")


def updateDatabase(request):
    # APIs request
    url = 'http://apis.is/cinema'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
   
    # Delete old movie-entries from db
    Showtime.objects.all().delete()
    Movie.objects.all().delete()

    # Insert newly fetched movies into db
    for movie in data['results']:
        if (movie['restricted']!=u"Öllum leyfð"):
            indexOfYear = movie['restricted'].find(u"ára")
            restrictedAge = int(movie['restricted'][0:indexOfYear])
        else:
            restrictedAge = 0

        m = Movie(title=movie['title'],
                    released=int(movie['released']), 
                    restricted=restrictedAge, 
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


def getMoviesFromDB(request):
    return Movie.objects.all().values()

def showMovies():
    johnWick = Movie.objects.filter(title='John Wick').values('title', 'restricted', 'released')
    restrictedTwelve = Movie.objects.filter(restricted=12).values('title')
    restrictedSixteen = Movie.objects.filter(restricted=16).values('title')

    print johnWick
    for i in range(0,len(restrictedTwelve)):
        print restrictedTwelve[i]['title']
    for i in range(0, len(restrictedSixteen)):
        print restrictedSixteen[i]['title']
    # movieList = getMoviesFromDB()
