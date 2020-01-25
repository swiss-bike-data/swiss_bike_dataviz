#!/bin/bash


for f in data/*.geojson; do
	cat $f | jq '.features[] | select(.properties.name == "ZH253843")'
done
