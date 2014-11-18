from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=50)
    released = models.IntegerField()
    restricted = models.IntegerField()
    imdb = models.CharField(max_length=20)
    image = models.URLField(max_length=30)
    #~ question_text = models.CharField(max_length=200)
    #~ pub_date = models.DateTimeField('date published')


class Showtime(models.Model):
    movie = models.ForeignKey(Movie)
    cinema = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    #~ choice_text = models.CharField(max_length=200)
    #~ votes = models.IntegerField(default=0)