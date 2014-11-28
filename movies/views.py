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
    todayShowtimes = Showtime.objects.values('movie')
    wmMovies = wm.movies.filter(id__in=todayShowtimes).all()
    otherMovies = Movie.objects.filter(id__in=todayShowtimes).exclude(id__in=wmMovies).all()
    
    #~ Render and return template with data.
    t = loader.get_template('index.html')
    c = Context({ 'theaterList':theaters, 'myMovies':wmMovies, 'allMovies':otherMovies })
    
    return HttpResponse( t.render(c) )

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
    if Timestamp.objects.exists():
        lastTime = Timestamp.objects.latest('timeFetched').timeFetched
    else:
        lastTime = 0
    
    # If there were less than 1 hour since the last
    # request we wont make another request ...
    if (time.time()-lastTime)>60*60:
        _requestMoviesFromApisAndSaveToDatabase(request)

def _requestMoviesFromApisAndSaveToDatabase(request):
    # APIs request
    url = 'http://apis.is/cinema'
    json_obj = urllib2.urlopen(url)
    data = json.load(json_obj)
    
    # Insert newly fetched movies into db
    for movie in data['results']:
        
        try:
            #~ Retrieving movie from database
            m = Movie.objects.get( title=movie['title'], released=int(movie['released']) )
        except Movie.DoesNotExist:
            #~ Prep work before actually adding movie to database
            if (movie['restricted']!=u"Öllum leyfð"):
                indexOfYear = movie['restricted'].find(u"ára")
                restrictedAge = int(movie['restricted'][0:indexOfYear])
            else:
                restrictedAge = 0
            
            #~ Adding movie to database
            m = Movie.objects.create(
                    title=movie['title'],
                    released=int(movie['released']), 
                    restricted=restrictedAge, 
                    imdb=movie['imdb'], 
                    image=movie['image'])
        
        #~ Updating showtimes for movie
        Showtime.objects.filter(movie=m).delete()
        for cinema in movie['showtimes']:
            for time in cinema['schedule']:
                Showtime.objects.create(movie=m, cinema=cinema['theater'], time=time)
    
    _updateTimestamp()

def _updateTimestamp():
    # Delete old timestamp from db
    Timestamp.objects.all().delete()

    # Get current time
    ts = time.time()

    # Save current time in db
    t = Timestamp(timeFetched=ts)
    t.save()
