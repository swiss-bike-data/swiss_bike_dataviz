#!/usr/bin/env python

# add column to dataframe to calculate distance between steps, per bike

import os
import pandas as pd
import numpy as np

# parameter to define a non-movement (e.g. 50 meters)
# this is to correct for GPS drift (any change in measurement is counted as "distance")
CUTOFF_METERS = 50.0

def main():

	iter_csv = pd.read_csv('..'+os.sep+'data'+os.sep+'_all_bikes.csv', sep=',', parse_dates=['timestamp'], iterator=True, chunksize=100000)
	df = pd.concat([chunk[chunk['provider'] == 'smide'] for chunk in iter_csv])

	#print(df.dtypes)
	df = df[['id','timestamp','longitude','latitude']]
	#print(df.head)

	# split
	df_g = df.groupby(['id'])
	
	# apply
	df_g = df_g.apply(dist_apply)

	# need to rename and reindex
	#print(df_g.columns.tolist())
	df_g.columns = ['id_g', 'timestamp', 'longitude', 'latitude', 'distance_km', 'total_distance_km']
	# reset index
	df_g = df_g.reset_index(level=[0,1])

	# rejoin
	#df = pd.concat([df,df_g.reset_index()],axis=1)
	df = pd.merge(df_g,df)
	#print(df)
	# print bike with max distance
	print('bike with max distance:')
	print(df[df.total_distance_km == df.total_distance_km.max()].tail(1))
	
	# export
	df.to_csv('smide_distance.csv',sep=',',index=False)

def dist_apply(group):
	# sort
	group.sort_values(by='timestamp',inplace=True)

	# get offset
	group['longitude_shift'] = group.longitude.shift()
	group['latitude_shift'] = group.latitude.shift()

	# calc distance
	group['distance_km'] = group.apply(lambda x: \
		haversine_np(lon1 = x.longitude, lat1 = x.latitude, \
		lon2 = x.longitude_shift, lat2 = x.latitude_shift), axis=1)

	# filter low distances
	group.loc[group.distance_km < CUTOFF_METERS * 0.001, 'distance_km'] = 0
	
	# calc running total of distance
	group['total_distance_km'] = group.distance_km.cumsum()
	
	# cleanup
	del group['longitude_shift']
	del group['latitude_shift']
	#del group['cutoff']

	return group

def haversine_np(lon1, lat1, lon2, lat2):
	# https://stackoverflow.com/a/29546836/2327328
	"""
	Calculate the great circle distance between two points
	on the earth (specified in decimal degrees)

	All args must be of equal length.    

	"""
	lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

	c = 2 * np.arcsin(np.sqrt(a))
	km = 6367 * c
	return km

if __name__ == "__main__":
	main()