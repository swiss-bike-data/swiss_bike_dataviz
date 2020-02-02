#!/usr/bin/env python
import pandas as pd
import folium

# https://gist.github.com/deparkes/9a0b45c69beb9a614f54d13bc7c551b5

df = pd.read_csv('smide_193.csv')
df = df[['latitude','longitude']]
points = [tuple(x) for x in df.to_numpy()]

ave_lat = sum(p[0] for p in points)/len(points)
ave_lon = sum(p[1] for p in points)/len(points)

# Load map centred on average coordinates
my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=14)

#add a markers
for each in points:  
    folium.Marker(each).add_to(my_map)

#fadd lines
folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)

# Save map
my_map.save("./smide.html")