#!/usr/bin/env bash

docker build . --tag bjarnijens/cinema
docker run -itd --rm -p 8123:80 bjarnijens/cinema