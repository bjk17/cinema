Lokaverkefni í áfanganum vefforritun við HÍ haustið 2014.
=========================================================

Ákveðið var að smíða vefsíðu sem að sækir gögn frá [APIs](http://docs.apis.is/)
um þær kvikmyndir sem er verið að sýna í bíóhúsum landsins og birtir notandanum.
Notandinn fær svo möguleika á að sía myndir út frá kvikmyndahúsum og vista myndir
í "Mínar myndir". Notandinn fær úthlutaða einstaka kennitölu og getur því heimsótt
síðuna aftur með þeirri kennitölu til að sjá aftur sínar myndir í "Mínum myndum".


Hýsing síðunnar
---------------

Síðan er hýst á Raspberry Pi model B örtölvu í heimahúsi og notast er við lénið
[bio.sudo.is](http://bio.sudo.is/).


Setja upp verkefnið
-------------------

    `git clone http://github.com/bjk17/Vefforritun.git`
    `pip install -r requirements.txt`


Stilla Apache á Raspberry Pi
----------------------------

Byrjað er að setja upp Apache: `sudo apt-get install apache2
libapache2-mod-wsgi`

Næst breytum við skránni `/etc/apache2/apache2.conf` með því að bæta við eftirfarandi línum:

```apache
## bio.sudo.is
# Serving our static folder with JS, CSS, etc.
Alias /static/movies/ /path/to/Vefforritun/movies/static/movies/
<Directory /path/to/Vefforritun/movies/static/movies/>
    # Apache/2.2.22
    Order deny,allow
    Allow from all
    
    # Apache/2.4
    #Require all granted
</Directory>

WSGIScriptAlias / /path/to/Vefforritun/Vefforritun/wsgi.py

# Daemon process to serve changes in your local directory in real time
# python-path should read from your virtualenv foulder
WSGIDaemonProcess / python-path=/path/to/Vefforritun:/path/to/.envs/bio/lib/python2.7/site-packages threads=5
WSGIProcessGroup /

<Directory /path/to/Vefforritun/Vefforritun/>
    <Files wsgi.py>
        Order deny,allow
        Allow from all
    </Files>
</Directory>
```

Loks þarf að endurræsa Apache þjónustunni: `sudo service apache2 reload`.
