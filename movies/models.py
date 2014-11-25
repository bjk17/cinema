# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50, primary_key=True)
    released = models.IntegerField(primary_key=True)
    restricted = models.IntegerField()
    imdb = models.CharField(max_length=20)
    image = models.URLField(max_length=30)
    
    unique_together = ("title", "released")
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, self.released)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie)
    cinema = models.CharField(max_length=50)
    time = models.CharField(max_length=20)
     
    def getCinema(self):
        reps = {u'á':'a', u'ð':'d', u'é':'e', u'í':'i', u'ó':'o', u'ú':'u', u'ý':'y', u'þ':'th', u'æ':'ae', u'ö':'o'}
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