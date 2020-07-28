# import necessary packages
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import earthpy as et
from shapely.geometry import  MultiLineString
import json

def main():
	all_paths = {}
	roads = gpd.read_file('data/ca_roads/roads.shp')
	print(roads)
	geometries = roads['geometry']
	for line_string in geometries:
		# print(type(line_string))
		if isinstance(line_string, MultiLineString):
			for single_line in line_string.geoms:
				add_path(all_paths, single_line)
		else:
			add_path(all_paths, line_string)
	all_paths = list(all_paths)
	json.dump(all_paths, open('data/ca_roads.json', 'w'))
	print(len(all_paths))

def add_path(all_paths, line_string):
	path = []
	for point in line_string.coords:
		path.append(point)
	all_paths(tuple(path))


if __name__ == '__main__':
	main()