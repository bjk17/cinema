#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, loader

from movies.models import Movie,Showtime,Timestamp

import sys, time, urllib2, json


def index(request):
    #Show theaters and movies on site
    requestMovies(request)
    theaters = getTheaters()
    allMovies = getMoviesFromDBWithShowtimes(request)
    # showtimes = []

    # for movie in allMovies:
    #     showtimes[movie].append(getShowtimeForMovie(movie))


            

    t = loader.get_template('index.html')
    c = Context({'theaterList': theaters, 'allMovies': allMovies})

    return HttpResponse(t.render(c))

def getTheaters():
    theaterList = {
        'bioParadis' : 'Bíó Paradís',
        'borgarbioAkureyri' : 'Borgarbíó Akureyri',
        'haskolabio' : 'Háskólabíó',
        'laugarasbio' : 'Laugarásbíó',
        'sambioinAkureyri' : 'Sambíóin Akureyri',
        'sambioinAlfabakka' : 'Sambíóin Álfabakka',
        'sambioinEgilshöll' : 'Sambíóin Egilshöll',
        'sambioinKeflavik' : 'Sambíóin Keflavík',
        'sambioinKringlunni' : 'Sambíóin Kringlunni',
        'sambioinSelfossi' : 'Sambíóin Selfossi',
        'smarabio' : 'Smárabíó', 
    }

    return theaterList

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
def getMoviesFromDBWithShowtimes(request):
    movies = []
    
    for movie in Movie.objects.all():
        showtimes = Showtime.objects.filter(movie=movie)
        movies.append({"Movie":movie, "Showtimes":showtimes})

    return movies
