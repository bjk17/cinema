#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, loader

from movies.models import Movie, Showtime, Timestamp
from watchmen.models import Watchman

import sys, time, uuid, urllib2, json

#~ http://bio.sudo.is/?id=0123456789usertest0123456789usertest
def index(request):
    #~ Retrieving ID from query string og redirecting user
    #~ to site with valid ID in query string.
    if 'id' not in request.GET:
        return _redirectToNewID(request)
    
    #~ Loading Watchman object with ID from query string.
    #~ If he doesn't exist we create a new one and redirect
    #~ user to site with its ID in query string.
    try:
        id = request.GET.get('id', None)
        wm = Watchman.objects.get(id=id)
    except Watchman.DoesNotExist:
        return _redirectToNewID(request)
    
    #~ Updating dabase and retrieving theaters and movies.
    _updateDataIfNeccessary(request)
    theaters = _getTheaters()
    wmMovies = wm.movies.all()
    otherMovies = Movie.objects.all().exclude(id__in=wmMovies)
    
    #~ Render and return template with data.
    t = loader.get_template('index.html')
    c = Context({'theaterList': theaters, 'myMovies': wmMovies, 'allMovies': otherMovies})
    
    return HttpResponse(t.render(c))

def _redirectToNewID(request):
    newID = str(uuid.uuid4())
    Watchman(id=newID).save()
    return redirect("/?id="+newID)

def _getTheaters():
    theaterList = {
        'Borgarbio' : 'Borgarbíó Akureyri',
        'Haskolabio' : 'Háskólabíó',
        'Laugarasbio' : 'Laugarásbíó',
        'SambioinAkureyri' : 'Sambíóin Akureyri',
        'SambioinAlfabakka' : 'Sambíóin Álfabakka',
        'SambioinEgilsholl' : 'Sambíóin Egilshöll',
        'SambioinKeflavik' : 'Sambíóin Keflavík',
        'SambioinKringlunni' : 'Sambíóin Kringlunni',
        'Smarabio' : 'Smárabíó',
    }

    return theaterList

def _updateDataIfNeccessary(request):
    # Get time last request was made and current time
    lastRequest = Timestamp.objects.values('timeFetched')
    currentTime = time.time()
    lastTime = 0
    
    if len(lastRequest)>0:
        lastTime = lastRequest[0]['timeFetched']
    
    # If there were less than 1 hour since the last
    # request we wont make another request ...
    if (currentTime-lastTime)>60*60:
        _requestMoviesFromApisAndSaveToDatabase(request)

def _requestMoviesFromApisAndSaveToDatabase(request):
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

        m = Movie(  title=movie['title'],
                    released=int(movie['released']), 
                    restricted=restrictedAge, 
                    imdb=movie['imdb'], 
                    image=movie['image'])
        m.save()
        
        for cinema in movie['showtimes']:
            for time in cinema['schedule']:
                s = Showtime(movie=m, cinema=cinema['theater'], time=time)
                s.save()
    
    _updateTimestamp()

def _updateTimestamp():
    # Delete old timestamp from db
    Timestamp.objects.all().delete()

    # Get current time
    ts = time.time()

    # Save current time in db
    t = Timestamp(timeFetched=ts)
    t.save()
