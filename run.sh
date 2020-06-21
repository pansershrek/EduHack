#!/bin/bash

docker-compose down
docker-compose up -d --build
sleep 20
docker exec focused_engelbart bash -c "./manage.py load_crit"