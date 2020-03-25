# get_publibike_timeseries

+ collect raw data from this repo: https://github.com/swiss-bike-data/get-zuerich-bikeshare-data

+ from that repo, run geojson2csv.py

+ that python script creates _all.csv, for which you can get only Publibike rows:

    head -1 _all_bikes.csv >> _publibike.csv && grep publibike _all_bikes.csv >> _publibike.csv

+ this script reads _publibike.csv