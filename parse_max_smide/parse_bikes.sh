#!/bin/bash

# not meant to be run, but to keep some interesting one-liners


# create csv for just one type of bikes
head -1 bikes.csv > smide.csv && grep smide bikes.csv >> smide.csv

# get total distance for each bike
head -1 smide_distance.csv > smide_distance_max.csv && grep "2020-02-01 21:58:35" smide_distance.csv >> smide_distance_max.csv

for f in data/*.geojson; do
	cat $f | jq '.features[] | select(.properties.name == "ZH253843")'
done
