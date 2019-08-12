# -*- coding: utf-8 -*-
from django.db import models
from movies.models import Movie


class Watchman(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    movies = models.ManyToManyField(Movie)
    
    def get_movies(self):
        return u"\n".join([m.title for m in self.movies.all()])
    
    def __unicode__(self):
        return u'id: %s (%s)' % (self.id, self.get_movies())
