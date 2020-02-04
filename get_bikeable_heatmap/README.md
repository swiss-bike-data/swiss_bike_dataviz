# get_bikeable_heatmap

this python3 code does the following:

+ scrapes the map data from [bikeable.ch](https://bikeable.ch/map) ([API endpoint](https://backend.bikeable.ch/api/v2/cachedlightentries))

+ gets bicycle fatalities in Switzerland, which is taken from [official raw data](https://data.geo.admin.ch/ch.astra.unfaelle-personenschaeden_alle/) and parsed and made available as [geojson in this repository](https://github.com/philshem/swiss_bike_deaths/blob/master/swiss_bike_deaths.geojson)

+ plots the bikeable data as a heatmap of dangerous spots

+ plots the bike deaths as points on the map

+ saves output to [static and local html file](https://github.com/philshem/get_bikes/blob/master/get_bikeable_heatmap/html/heatmap.html)

## view demo

[interactive map](https://rawcdn.githack.com/philshem/get_bikes/6dc0da1aac2a15e3aa0e46b95453a827541ac612/get_bikeable_heatmap/html/heatmap.html)

## screenshot

![screenshot of heatmap](https://raw.githubusercontent.com/philshem/get_bikes/master/get_bikeable_heatmap/html/heatmap_screenshot.png)