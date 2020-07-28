from SimpleTable import SimpleTable
from util import *
import time
import sys
import os
"""
Rate limits:
Elevation linestrings (2.000 requests per day @40 requests per minute)
Directions (2.000 requests per day @40 requests per minute)
40/min means you should pause >= 1.5s between requests

https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248b44db44b33c64508afa658b8673c9580&start=8.681495,49.41461&end=8.687872,49.420318
"""

def main():
	turn_on_cache('cache/nearBay.pkl')
	cities = SimpleTable('data/us_cities_clean.csv').to_dict('Name')
	while True:
		city_a = input('City A: ')
		city_b = input('City B: ')
		add_path(cities, city_a, city_b)


def add_path(cities, city_a, city_b):
	gps_a = get_gps(cities, city_a)
	gps_b = get_gps(cities, city_b)
	# gps_a = '-116.570188,31.880812'
	# gps_b = '-115.741188,30.053437'
	key = city_a +',' + city_b
	path = get_route_with_elevation(key, gps_a, gps_b)
	if path != None:
		print('success')
		os.system('python make_highway_graph_v2.py')
		# os.system('python pickleToJson.py')
	else:
		print('failed')

def get_gps(cities, city_name):
	if city_name in cities:
		return cities[city_name]['Coords']
	print('Unknown city ' + city_name)
	return input('Enter GPS: ')

if __name__ == '__main__':
	main()