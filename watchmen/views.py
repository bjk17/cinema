from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from movies.models import Movie
from watchmen.models import Watchman

import uuid

# Create your views here.
def index(request):
    #~ qs = request.META["QUERY_STRING"]
    
    if not 'id' in request.GET:
        ID = str(uuid.uuid4())
        Watchman(id=ID).save()
        return redirect("/wm/?id="+ID)
    
    ID = request.GET.get('id')
    
    try:
        wm = Watchman.objects.get(id=ID)
        return HttpResponse( 'id: ' + ID + '</br> Movies: ' + wm.get_movies() )
    except Watchman.DoesNotExist:
        return HttpResponse( 'id: ' + ID + '</br> User does not exist.' )

def id(request):
    ID = request.GET.get('id', 'None')
    return HttpResponse( '<h1>id</h1>' + '<p>' + ID + '</p>' )
    
def add(request):
    id = request.GET.get('id', None)
    movieID = request.GET.get('movie', None)
    
    try:
        wm = Watchman.objects.get(id=id)
    except Watchman.DoesNotExist:
        return HttpResponse("Error: Watchman object with id=%s doesn't exist!" % (id,) )
    
    try:
        movie = Movie.objects.get(id=movieID)
    except:
        return HttpResponse("Error: Couldn't retrieve %s movie from database!" % (movieID,) )
    
    try:
        wm.movies.add(movie)
    except:
        return HttpResponse("Error: Couldn't add %s movie to watchman object!" % (movie,) )
    
    return HttpResponse("Success: %s movie successfully added to watchman object with id=%s" % (movie, id,) )

def remove(request):
    id = request.GET.get('id', None)
    movieID = request.GET.get('movie', None)
    
    try:
        wm = Watchman.objects.get(id=id)
    except Watchman.DoesNotExist:
        return HttpResponse("Error: Watchman object with id=%s doesn't exist!" % (id,) )
    
    try:
        movie = Movie.objects.get(id=movieID)
    except:
        return HttpResponse("Error: Couldn't retrieve %s movie from database!" % (movieID,) )
    
    try:
        wm.movies.remove(movie)
    except:
        return HttpResponse("Error: Couldn't remove %s movie from watchman object!" % (movie,) )
    
    return HttpResponse("Success: %s movie successfully removed from watchman object with id=%s" % (movie, id,) )