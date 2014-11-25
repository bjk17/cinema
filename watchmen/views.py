from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

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
    
    #~ if not 'id' in request.GET:
        #~ ID = str(uuid.uuid4())
        #~ Watchman(id=ID).save()
        #~ return redirect("/wm/?id="+ID)
    #~ 
    #~ 
    #~ try:
        #~ wm = Watchman.objects.get(id=ID)
        #~ return HttpResponse( 'id: ' + ID + '</br> Movies: ' + wm.get_movies() )
    #~ except Watchman.DoesNotExist:
        #~ return HttpResponse( 'id: ' + ID + '</br> User does not exist.' )