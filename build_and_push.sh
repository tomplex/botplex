#!/usr/bin/env bash

$(aws ecr get-login --no-include-email)

docker build -t botplex:latest .
docker tag botplex:latest $ECR/botplex:latest

docker push $ECR/botplex:latest