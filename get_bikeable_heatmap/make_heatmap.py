#!/usr/bin/env python

# scrape bikeable data, convert to heatmap of problem spots
# collect swiss bike deaths, plot on same map

import os
import pandas as pd
import json
import requests
import folium
from folium.plugins import HeatMap

def main():

	# bikeable data as dataframe
	g1 = 'https://backend.bikeable.ch/api/v2/cachedlightentries'
	df_bi = get_bikeable(g1)

	# swiss bike accidents as dataframe
	g2 = 'https://raw.githubusercontent.com/philshem/swiss_bike_deaths/master/swiss_bike_deaths.geojson'
	df_sd = get_accidents(g2)
	
	# save them to an html map
	html = plot_points(df_sd, df_bi)
	print(html)

def plot_points(df_points, df_heatmap):

	max_amount = 1 # set this count to 1, since frequenices are discrete already. #float((group.total).max())

	# in case you want the map auto_centering, you have to create average or median points to start with
	#points = [tuple(x) for x in df_points[['latitude','longitude']].to_numpy()]
	#ave_lat = sum(p[0] for p in points)/len(points)
	#ave_lon = sum(p[1] for p in points)/len(points)

	# set custom icon
	#gicon = folium.features.CustomIcon('file:///home/philshem/fun/swiss_bike_deaths/get_bikeable/html/skull-crossbones.svg',icon_size=(14, 14))
	#gicon = folium.features.CustomIcon('https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg',icon_size=(14, 14))
	#gicon = folium.features.CustomIcon('http://www.pngall.com/wp-content/uploads/2016/05/Iron-Man.png', icon_size=(50,50))
	#icon_path = "/home/philshem/fun/swiss_bike_deaths/get_bikeable/html/skull-crossbones.png"
	#gicon = folium.features.CustomIcon(icon_image=icon_path ,icon_size=(50,50))

#	import copy
	#m = folium.Map()
	#icon_path = r"C:\some_path\icon.png"
	#marker=folium.Marker([row["coord"].y,row["coord"].x],popup=popup,icon=icon).add_to(feature_groups[alert_icon_name])

	# center and zoom on Zürich
	hmap = folium.Map(location=[47.385227, 8.537996],
			zoom_start=13,
			#tiles='Cartodb dark_matter',
			zoomControl = False)

	# to see available columns for popup
	#print(df_points.columns)

	# https://map.geo.admin.ch/?ch.astra.unfaelle-personenschaeden_fahrraeder=AD6D967DE2ED0150E0430A8394270150

	# add points to map (swiss bike deaths)
	for _, row in df_points.iterrows():

		popup_text = '''
		{0}<br><br>
		{1}<br><br>
		{2}<br>
		{3} {4} ({5})<br><br>
		<a href=" https://map.geo.admin.ch/?ch.astra.unfaelle-personenschaeden_fahrraeder={6}">View on geo.admin.ch</a><br>
		'''

		# generate text for tooltip
		popup_text = popup_text.format(row['AccidentType_en'], \
										row['RoadType_en'], \
										row['AccidentWeekDay_en'], \
										row['AccidentMonth_en'], \
										row['AccidentYear'], \
										row['AccidentHour_text'], \
										row['_id'] \
										)

		# weird: custom local icon needs to be initialized each pass through the loop
		# https://github.com/python-visualization/folium/issues/744#issuecomment-336036822
		gicon = folium.features.CustomIcon(icon_image='./html/skull-crossbones.png', icon_size=(25, 30))
		# icon source is font-awesome v5, which isn't supported in folium
		# for that reason, download the full font set, extract the specific one, save as local svg, 
		# and use imagemagick function "convert" to convert to png
		# > convert -background none -density 1200 -resize 25x30 html/skull-crossbones.svg html/skull-crossbones.png
		# adding font-awesome icons to folium map, only works for v4
		# https://stackoverflow.com/a/58609263/2327328

		folium.Marker([row['latitude'], row['longitude']],
							radius=15,
							icon=gicon,
							popup=folium.Popup(html=popup_text, max_width=450)  
							).add_to(hmap)

		continue #end loop over markers/points

	# add heatmap from grouped dataframe (bikeable)
	# https://gist.github.com/deparkes/9a0b45c69beb9a614f54d13bc7c551b5
	hm_wide = HeatMap( list(zip(df_heatmap.latitude.values, df_heatmap.longitude.values, df_heatmap.latitude.values)), 
			min_opacity=0.2, #max_val=max_amount,
			radius=12, blur=15,
			max_zoom=1, 
			)

	hmap.add_child(hm_wide)

	# Save map locally
	html = "./html/heatmap.html"
	hmap.save(html)
	
	return html

def get_accidents(url):

	data = get_json(url)

	# load json into dataframe	
	df = pd.json_normalize(data.get('features'))
	
	# unpack geocoords
	df[['longitude', 'latitude','tmp']] = pd.DataFrame(df['geometry.coordinates'].tolist(), columns=['longitude', 'latitude','tmp'])

	# delete columns not needed
	del df['tmp']
	del df['geometry.coordinates']
	del df['geometry.type']
	del df['type']


	# rename columns
	df.columns = df.columns.str.replace('properties.', '')
	df.rename(columns={'AccidentUID':'_id'}, inplace=True)	
	df['url'] = url

	return df

def get_bikeable(url):
	
	data = get_json(url)

	# load json into dataframe	
	df = pd.json_normalize(data.get('data'))

	# filter on famed=False (bad spots) and gotFixed=False (not fixed)
	df = df[(df.famed == False)]
	df = df[(df.gotFixed == False)]

	# drop columns
	del df['famed']
	del df['gotFixed']

	# rename columns
	df.rename(columns={'_id':'_id','coords.lat': 'latitude', \
							'coords.lng': 'longitude'}, \
							inplace=True)
	df['url'] = url

	return df

def get_json(url):
	
	# return json object from http request
	data = requests.get(url).json()
	return data

if __name__ == "__main__":
	main()