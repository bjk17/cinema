from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    restricted = models.IntegerField()
    imdb = models.CharField(max_length=20)
    image = models.URLField(max_length=30)

class Showtime(models.Model):
    movie = models.ForeignKey(Movie)
    cinema = models.CharField(max_length=50)
    time = models.CharField(max_length=20)

class Timestamp(models.Model):
	timeFetched = models.FloatField()
