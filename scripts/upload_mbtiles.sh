#!/bin/bash

pipenv run python upload2openafrica.py \
  --key ${CKAN_API_KEY} \
  --org "narwassco" \
  --pkg narok-water-vectortiles \
  --title "Vector Tiles for water supply systems in Narok, Kenya" \
  --file ../data/narok.mbtiles \
  --desc "mbtiles format of Mapbox Vector Tiles which was created by tippecanoe."
