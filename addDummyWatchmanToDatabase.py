from movies.models import Movie
from watchmen.models import Watchman
import uuid

movies = Movie.objects.all()

id = str(uuid.uuid4())
print "id:", id

wm = Watchman(id=id)
wm.save()

#~ wm.movies.add(movies)
for m in movies:
    wm.movies.add(m)


#~ print "wm.get_movies()", wm.get_movies()
print "wg.movies.all()"
for m in wm.movies.all():
    print m



#~ s1.save()
#~ 
#~ s2 = Showtime(movie=m, cinema="Laugarásbíó", time="20:00")
#~ s2.save()
#~ 
#~ s3 = Showtime(movie=m, cinema="Laugarásbíó", time="22:00")
#~ s3.save()