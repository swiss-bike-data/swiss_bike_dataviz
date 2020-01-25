#!/usr/bin/env python

# parse geojson files to csv

import os
import glob
import json
import pandas as pd

def main():

	files = glob.glob('..'+os.sep+'data'+os.sep+'*.geojson')

	frames = []
	for f in files:
		with open(f,'r') as fo:
			data = json.load(fo)
		df = pd.io.json.json_normalize(data.get('features'))
		df['longitude'], df['latitude'] = zip(*df['geometry.coordinates'])
		df['timestamp'] = df['properties.time'].combine_first(df['properties.timeStamp'])
		# "01/25/2020, 21:51:45"
		df['timestamp'] = pd.to_datetime(df.timestamp, format='%m/%d/%Y, %H:%M:%S', errors='ignore')

		del df['properties.time']
		del df['properties.timeStamp']
		del df['geometry.coordinates']
		del df['geometry.type']
		del df['properties.address']
		del df['properties.zip']
		del df['type']

		df.rename(columns={'properties.range': 'range', \
							'properties.charge': 'charge', \
							'properties.manual': 'manual', \
							'properties.electric': 'electric', \
							'properties.id': 'id', \
							'properties.name': 'name', \
							'properties.provider': 'provider', \
							'properties.size': 'size'}, \
							inplace=True)

		df['filename'] = f.split(os.sep)[-1]
		#print(df.columns)
		#df['timestamp'].to_csv('test.csv')
		#break

		frames.append(df)

	df = pd.concat(frames)
	df.to_csv('bikes.csv',sep='\t')

if __name__ == "__main__":
	main()