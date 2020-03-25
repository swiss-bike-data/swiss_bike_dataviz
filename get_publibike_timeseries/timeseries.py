#!/usr/bin/env python

'''
plot timeseries of available publibikes in city zürich
'''

import os, glob
import pandas as pd
import datetime, time

def main():

	# load csv and keep only publibikes
	#iter_csv = pd.read_csv('..'+os.sep+'..'+'get-zuerich-bikeshare-data'+os.sep+'data'+os.sep+'_all_bikes.csv', sep=',', parse_dates=['timestamp'], iterator=True, chunksize=100000)
	#df = pd.concat([chunk[chunk['provider'] == 'publibike'] for chunk in iter_csv])

	# much faster with grep
	# head -1 _all_bikes.csv >> _publibike.csv && grep publibike _all_bikes.csv >> _publibike.csv
	iter_csv = pd.read_csv('_publibike.csv', sep=',', parse_dates=['timestamp'], iterator=True, chunksize=100000)
	df = pd.concat([chunk for chunk in iter_csv])

	# lose some columns
	df['total'] = df['electric'] + df['manual']
	df = df[['timestamp','latitude','longitude','total']]
	
	# truncate minutes and seconds
	df['timestamp'] = df.timestamp.dt.round('D')
	
	# calculate hourly average for each station
	df = df.groupby([df.timestamp, df.latitude, df.longitude]).mean()

	# calculate sum of all stations per hour
	df.reset_index(inplace=True)
	df = df[['timestamp','total']]

	# get daily sum over all stations
	df = df.groupby([df.timestamp]).sum()

	ax = df.plot(linestyle="",marker="o")
	fig = ax.get_figure()
	ax.set_xlabel('')
	ax.set_ylabel('Available Publibikes in Zürich (of ~1629 total)')
	ax.get_legend().remove()
	fig.savefig('_publibikes.png')


if __name__ == "__main__":
	main()