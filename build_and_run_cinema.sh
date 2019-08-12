#!/usr/bin/env bash

docker stop cinemaserver || echo "Cinema server not running"
docker build . --tag bjarnijens/cinema
docker run -itd --rm --name cinemaserver -p 8123:80 bjarnijens/cinema
