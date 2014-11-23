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

    def __unicode__(self):
        return u'%s %s' % (self.cinema, self.time)

class Timestamp(models.Model):
    timeFetched = models.FloatField()
