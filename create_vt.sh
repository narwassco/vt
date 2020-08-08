#!/bin/bash

docker-compose up
git add .
git commit -m "update vectortiles"
git push origin master