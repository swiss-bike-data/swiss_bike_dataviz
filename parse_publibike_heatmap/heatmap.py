#!/usr/bin/env python

# based on https://github.com/mikecunha/pygeo_heatmap/blob/master/geo_heatmap.ipynb

import os, glob
import pandas as pd
import datetime, time
import folium
from folium.plugins import HeatMap
from folium.features import MacroElement, Template
from selenium import webdriver

debug = False
SCALING_MAX = 0.5 # make the heatmap less heated
SLEEP_SEC = 1.0 # give time to download map tiles

def main():

	# remove existing scratch files
	clean_results()

	# load csv and keep only publibikes
	iter_csv = pd.read_csv('..'+os.sep+'data'+os.sep+'_all_bikes.csv', sep=',', parse_dates=['timestamp'], iterator=True, chunksize=100000)
	df = pd.concat([chunk[chunk['provider'] == 'publibike'] for chunk in iter_csv])

	# lose some columns
	df['total'] = df['electric'] + df['manual']
	df = df[['filename','timestamp','latitude','longitude','total']]

	# consider resampling and filling missing points, since from the scrape a couple files may be missing
	# https://stackoverflow.com/a/43777934/2327328

	if debug:
		# keep only weekdays for testing heatmap
		df = df[(df['timestamp'] >= pd.Timestamp('2020-01-30 12:00:00')) & (df['timestamp'] <= pd.Timestamp('2020-01-30 14:00:00'))]

	# create groups for individual heatmaps based on filename (time of crawling)
	grouped = df.groupby(['filename'])

	filename_list = []
	print ('rendering data to html...')

	for filename, group in grouped:
		f = 'results'+os.sep+'publibike_'+filename.replace('.geojson','.html')
			
		# get normalization amount
		max_amount = float((group.total).max())

		# plot difference to average bikes
		#group['total_diff'] = (group.total - group.total.mean()) / group.total
		
		# center and zoom on Zürich
		hmap = folium.Map(location=[47.385227, 8.537996],
				zoom_start=13,
				tiles='Cartodb dark_matter',
				zoomControl = False)

		# add heatmap from grouped dataframe
		hm_wide = HeatMap( list(zip(group.latitude.values, group.longitude.values, group.total.values)), 
				min_opacity=0.2,
				max_val=max_amount * SCALING_MAX,
				#radius=17, blur=15, 
				radius=17, blur=15,
				max_zoom=1, 
				)

		hmap.add_child(hm_wide)

		# add timestamp to html
		ts = filename.replace('.geojson','').replace('_','')
		dow = datetime.datetime.strptime(ts[:8], '%Y%m%d').strftime('%A')
		ts = '{5} {0}-{1}-{2} {3}:{4}'.format(ts[:4], ts[4:6], ts[6:8], ts[8:10], ts[10:12], dow)

		folium.map.Marker(
			[47.381389, 8.589107],
			icon=DivIcon(
				size=(250,36),
				anchor=(150,0),
				html=ts.replace(' ','<br>'),
				style="""
					font-size:36px;
					color:white;
					background-color: transparent;
					border-color: transparent;
					text-align: center;
					"""
				)
			).add_to(hmap)

		hmap.save(f)
		
		# add html file path to list for later
		filename_list.append(f)
		print (filename,ts)

		# debugging
		if debug and len(filename_list) >= 100:
			break

	# save html as png
	if True:
		driver = init_browser()
		print ('converting html to png...')

		for f in filename_list:
			p = html2png(f,driver)
			print(p)

		close_browser(driver)

def clean_results(fp='results'):

	cleanlist = glob.glob(os.path.join(fp, "*.png"))
	cleanlist += glob.glob(os.path.join(fp, "*.html"))

	for f in cleanlist:
		os.remove(f)
	return

def init_browser():

	# requires chromedriver
	options = webdriver.ChromeOptions()
	#options.add_argument("--start-maximized")
	options.add_argument("--headless")
	options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
	chrome_driver_binary = "/usr/local/bin/chromedriver"
	return webdriver.Chrome(chrome_driver_binary, options=options)

def close_browser(d):
	d.quit()
	return

def html2png(html,driver):
	png = html.replace('.html','.png')
	driver.get('file:///'+os.getcwd()+os.sep+html)
	if not debug:
		time.sleep(SLEEP_SEC)
	driver.save_screenshot(png)
	return png

class DivIcon(MacroElement):
	# https://nbviewer.jupyter.org/gist/BibMartin/ec2a96034043a7d5035b
	def __init__(self, html='', size=(30,30), anchor=(0,0), style=''):
		"""TODO : docstring here"""
		super(DivIcon, self).__init__()
		self._name = 'DivIcon'
		self.size = size
		self.anchor = anchor
		self.html = html
		self.style = style

		self._template = Template(u"""
			{% macro header(this, kwargs) %}
			  <style>
				.{{this.get_name()}} {
					{{this.style}}
					}
			  </style>
			{% endmacro %}
			{% macro script(this, kwargs) %}
				var {{this.get_name()}} = L.divIcon({
					className: '{{this.get_name()}}',
					iconSize: [{{ this.size[0] }},{{ this.size[1] }}],
					iconAnchor: [{{ this.anchor[0] }},{{ this.anchor[1] }}],
					html : "{{this.html}}",
					});
				{{this._parent.get_name()}}.setIcon({{this.get_name()}});
			{% endmacro %}
			""")

if __name__ == "__main__":
	main()