import json
import pickle
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import earthpy as et
from shapely.geometry import  MultiLineString
import json
import arcgis 
"""
round to 5 decimal places
"""

def main2():

	lyrFile = arcgis.LayerFile(r"data/ca_elevation/data/elevation.lyr")
	for lyr in lyrFile.listLayers():
	    if lyr.supports("datasource"):
	        if lyr.isBroken:
	            print(lyr.name)

def main():
	all_highways = json.load(open('client/ca_roads.json', 'r'))
	print(len(all_highways))
	some_saved_data = pickle.load(open('cache/nearBay.pkl', 'rb'))

	elevation_cache = record_saved_elevations(some_saved_data)
	# elevations = gpd.read_file('data/NED60M_SpatialMetadata/NED60M_fe2898_October2018.shp')

	# x = elevations['geometry']
	# for y in x:
		# print(y)
	# print(x)
	cache_hits = 0
	cache_misses = 0

	for highway in all_highways:
		for point in highway:
			point = normalize_point(point)
			if point in elevation_cache:
				cache_hits += 1
			else:
				cache_misses += 1
	print(cache_hits, cache_misses)

def normalize_point(point):
	lng = round(point[0], 4)
	lat = round(point[1], 4)
	return (lng, lat)

def record_saved_elevations(some_saved_data):
	elevation_cache = {}

	for key in some_saved_data:
		path = some_saved_data[key]
		if path == None: continue
		for point in path:
			elevation = point[2]
			gps = normalize_point(point)
			elevation_cache[gps] = elevation
	return elevation_cache


if __name__ == '__main__':
	main()