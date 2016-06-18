# Lokaverkefni í áfanganum vefforritun við HÍ haustið 2014.

Ákveðið var að smíða vefsíðu sem að sækir gögn frá [APIs](http://docs.apis.is/)
um þær kvikmyndir sem er verið að sýna í bíóhúsum landsins og birtir notandanum.
Notandinn fær svo möguleika á að sía myndir út frá kvikmyndahúsum og vista myndir
í "Mínar myndir". Notandinn fær úthlutaða einstaka kennitölu og getur því heimsótt
síðuna aftur með þeirri kennitölu til að sjá aftur sínar myndir í "Mínum myndum".


### Hýsing síðunnar

Síðan er hýst á Raspberry Pi model B örtölvu í heimahúsi og notast er við lénið
[bio.bjk.is](http://bio.bjk.is/) (áður [bio.sudo.is](http://bio.sudo.is/)).
Vegna takmarkaðs vélbúnaðar er síðan nokkuð hægvirk, og þá sérstaklega þegar
kvikmyndir í flýtiminni (e. cache) eru uppfærðar þar sem þær eru geymdar í SQLite
gagnagrunni á hægvirku microSD minniskorti.


## Uppsetning síðunnar á Raspberry Pi

### Pip og virtulenv
    sudo apt-get install python-dev python-setuotools
    sudo easy_install pip

*Aths. Það gæti verið að `python-dev` pakkinn sé óþarfi.*

    sudo pip install virtualenv virtualenvwrapper

Fylgja svo [þessum leiðbeiningum](http://virtualenvwrapper.readthedocs.org/en/latest/).

    mkvirtualenv django_bio
    workon django_bio

### Sækja kóðann

    git clone http://github.com/bjk17/cinema.git
    cd cinema
    pip install -r requirements.txt

### Stilla Apache á Raspberry Pi

    sudo apt-get install apache2 libapache2-mod-wsgi

Við bætum síðunni við sem *site* í Apache.

    sudo touch /etc/apache2/sites-available/bio.bjk.is
    sudo nano /etc/apache2/sites-available/bio.bjk.is

Afritið eftirfarandi inn í tóma skjalið:

```apache
<VirtualHost *:80>
  ServerName  bio.bjk.is
  ServerAlias bio.sudo.is

  # Serving our static folder with JS, CSS, etc.
  Alias /static/movies/ /path/to/cinema/movies/static/movies/
  <Directory /path/to/cinema/movies/static/movies/>
    <IfVersion < 2.4>
      Order deny,allow
      Allow from all
    </IfVersion>
    <IfVersion >= 2.4>
      Require all granted
    </IfVersion>
  </Directory>

  WSGIScriptAlias / /path/to/cinema/cinema/wsgi.py

  # Daemon process to serve changes in your local directory in real time
  # python-path should read from your virtualenv foulder
  WSGIDaemonProcess / python-path=/path/to/cinema:/path/to/.envs/bio/lib/python2.7/site-packages threads=5
  WSGIProcessGroup /

  <Directory /path/to/cinema/cinema/>
    <Files wsgi.py>
      Order deny,allow
      Allow from all
    </Files>
  </Directory>
</VirtualHost>
```

Loks þarf að skrá síðuna og endurræsa Apache þjónustunni.

    sudo a2ensite bio.bjk.is
    sudo service apache2 reload
