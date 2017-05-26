#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, loader
from django.conf import settings

from movies.models import Movie, Showtime, Timestamp
from watchmen.models import Watchman

import os, sys, time, uuid, urllib2, json, datetime

def index(request):
    #~ Retrieving ID from query string and redirecting user
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
    wmMovies = wm.movies.filter(id__in=todayShowtimes).all().order_by('-imdb', 'title')
    otherMovies = Movie.objects.filter(id__in=todayShowtimes).exclude(id__in=wmMovies).all().order_by('-imdb', 'title')
    
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

    timeNow = time.time()

    dateNow = datetime.datetime.fromtimestamp(timeNow).date();
    lastDate = datetime.datetime.fromtimestamp(lastTime).date()

    # If there were less than 1 hour since the last
    # request we wont make another request 
    # or if the request is on a new day ...
    if (timeNow-lastTime)>60*60 or lastDate < dateNow:
        _requestMoviesFromApisAndSaveToDatabase(request)

def _requestMoviesFromApisAndSaveToDatabase(request):
    # APIs request

    ## apis.is/cinema endpoint is down, using cached content
    # try:
    #     url = request.scheme+'://apis.is/cinema'
    #     req = urllib2.Request(url)
    #     json_obj = urllib2.urlopen(req)
    #     data = json.load(json_obj)
    # except urllib2.URLError as e:
    #     import logging
    #     logging.error("url request: "+url)
    #     logging.error(e)
    #     return
    json_file = os.path.join(settings.BASE_DIR, "data", "cinema_2014-11-28.json")
    json_cont = open(json_file).read()
    data = json.loads(json_cont)

    # Remove all showtimes in order to delete movies that are not in cinemas
    Showtime.objects.all().delete()

    # Insert newly fetched movies into db
    for movie in data['results']:
        try:
            #~ String contains a 4-digit year
            stringReleased = movie['released']
            indexOfYear = min(  stringReleased.find(u"1"),
                                stringReleased.find(u"2") )
            try:
                releasedYear = int(stringReleased[indexOfYear::4])
            except ValueError:
                from datetime import datetime
                releasedYear = datetime.now().year
            
            #~ Retrieving movie from database
            m = Movie.objects.get( title=movie['title'], released=releasedYear )
            #~ Update IMDb score each time
            Movie.objects.filter( title=movie['title'], released=releasedYear ).update( imdb=movie['imdb'] )
        except Movie.DoesNotExist:
            #~ Prep work before actually adding movie to database
            if (movie['restricted']!=u"Öllum leyfð"):
                stringRestricted = movie['restricted']
                indexOfYear = stringRestricted.find(u"ára")
                try:
                    restrictedAge = int(stringRestricted[0:indexOfYear])
                except ValueError:
                    restrictedAge = 0
            else:
                restrictedAge = 0
            
            #~ Adding movie to database
            m = Movie.objects.create(
                    title=movie['title'],
                    released=releasedYear, 
                    restricted=restrictedAge, 
                    imdb=movie['imdb'], 
                    image=movie['image'],
                    imdbLink=movie['imdbLink'])
        
        #~ Updating showtimes for movie
        Showtime.objects.filter(movie=m).delete()
        for cinema in movie['showtimes']:
            for time in cinema['schedule']:
                Showtime.objects.create(movie=m, cinema=cinema['theater'], time=time)

    # If there are no showtimes for movie, it is not in theaters
    for movie in Movie.objects.all():
        if not movie.getShowtimeList():
            movie.delete()

    _updateTimestamp()

def _updateTimestamp():
    # Delete old timestamp from db
    Timestamp.objects.all().delete()

    # Get current time
    ts = time.time()

    # Save current time in db
    t = Timestamp.objects.create(timeFetched=ts)
