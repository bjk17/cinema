# An Icelandic cinema movie-showtime webscraper and viewer
[![Build Status](https://travis-ci.org/bjk17/cinema.svg?branch=master)](https://travis-ci.org/bjk17/cinema)

__*\*Be aware!\* Due to changes to {apis.is} endpoint we're currently serving cached data from 2014-11-28.*__

*Original Icelandic REAMDE text*
> Ákveðið var að smíða vefsíðu sem að sækir gögn frá [APIs](http://docs.apis.is/)
> um þær kvikmyndir sem er verið að sýna í bíóhúsum landsins og birtir notandanum.
> Notandinn fær svo möguleika á að sía myndir út frá kvikmyndahúsum og vista myndir
> í "Mínar myndir". Notandinn fær úthlutaða einstaka kennitölu og getur því heimsótt
> síðuna aftur með þeirri kennitölu til að sjá aftur sínar myndir í "Mínum myndum".


## Deployment and hosting

The project is hooked into [Docker Hub](https://hub.docker.com/r/bjarnijens/cinema/) 
for automated builds and for hosting image artefacts. The newest Docker image is (manually) 
fetched and run on a (personal and multi-purpose) VPS. The docker container is exposed via 
an Apache web server (using a free SSL certificate from [Let's Encrypt](https://letsencrypt.org)) 
under the URL [bio.bjk.is](https://bio.bjk.is/).

[Travis CI](https://travis-ci.org/bjk17/cinema) integration have been added to run the (currently 
non-existant) unit tests on every commit. It also tries to build the Docker image, just because we can.
