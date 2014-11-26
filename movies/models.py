# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    restricted = models.IntegerField()
    imdb = models.CharField(max_length=20)
    image = models.URLField(max_length=30)
    
    unique_together = ("title", "released")
    
    def getShowtimeList(self):
        showtimes = Showtime.objects.filter(movie=self)
        dictionary = {}
        for st in showtimes:
            cinema = st.cinema
            if cinema in dictionary:
                dictionary[cinema].append(st.time)
            else:
                dictionary[cinema]=[st.time]
        return dictionary
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.released)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie)
    cinema = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
     
    def getCinema(self):
        reps = {u'Á':'A', u'á':'a', u'ð':'d', u'É':'E', u'é':'e', u'Í':'I', u'í':'i', u'Ó':'O', u'ó':'o', u'Ú':'U', u'ú':'u', u'Ý':'Y', u'ý':'y', u'Þ':'Th', u'þ':'th', u'Æ':'Ae', u'æ':'ae', u'Ö':'O', u'ö':'o', u' ':''}
        cinema = replace_all(self.cinema,reps)
        return u'%s' % (cinema,)

    def __unicode__(self):
        return u'%s %s' % (self.cinema, self.time)

class Timestamp(models.Model):
    timeFetched = models.FloatField()

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text