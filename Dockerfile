FROM ubuntu:16.04

MAINTAINER Bjarni Jens Kristinsson <bjarni.jens@gmail.com>

RUN apt-get -y update && \
    apt-get -y full-upgrade && \
    apt-get -y install apache2 libapache2-mod-wsgi python-pip && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/cinema

# Caching the pip install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copying rest of source code
COPY . .

RUN touch data/database.db && chmod -R ugo+w data/ && \ 
    mkdir movies/migrations && touch movies/migrations/__init__.py && \
    mkdir watchmen/migrations && touch watchmen/migrations/__init__.py && \
    ./manage.py makemigrations && ./manage.py migrate

COPY apache.conf  /etc/apache2/sites-available/cinema.conf
RUN a2dissite 000-default && a2ensite cinema

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]