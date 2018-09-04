#!/usr/bin/env bash

docker build -t botplex .
docker run -v $PWD/log:/botplex/log --rm --name botplex_prod -p 8001:8000 botplex
