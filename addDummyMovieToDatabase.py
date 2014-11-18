from movies.models import Movie,Showtime

m = Movie(title="jOBS", released=2013, restricted=12, imdb="5.5/10  9,907 atkv.", image="http://kvikmyndir.is/images/poster/8497_500.jpg")
m.save()

s1 = Showtime(movie=m, cinema="Borgarbíó", time="22:00")
s1.save()

s2 = Showtime(movie=m, cinema="Laugarásbíó", time="20:00")
s2.save()

s3 = Showtime(movie=m, cinema="Laugarásbíó", time="22:00")
s3.save()