from SimpleTable import SimpleTable
from util import *
import time
"""
Rate limits:
Elevation linestrings (2.000 requests per day @40 requests per minute)
Directions (2.000 requests per day @40 requests per minute)
40/min means you should pause >= 1.5s between requests

https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248b44db44b33c64508afa658b8673c9580&start=8.681495,49.41461&end=8.687872,49.420318
"""

def main():
	cities = SimpleTable('data/ca_low.csv').to_dict('Name')
	turn_on_cache('cache/driving.pkl')

	route_cache = {}
	# # note that all city names in CA are unique
	cities = SimpleTable('data/ca_cities.csv').to_dict('Name')
	sorted_by_haversine = sort_by_haversine(cities)
	n = 0
	for city in sorted_by_haversine:
		print(n,city)
		key = 'Palo Alto' + ',' + city
		coord = cities[city]['Coords']
		route = get_route_with_elevation(key, PALO_ALTO, coord)
		# dont overload the server
		n += 1


def sort_by_haversine(cities):
	haversine_dict = {}
	# print(cities)
	for name, city in cities.items():
		coords = city['Coords']
		h_dist = haversine(coords, PALO_ALTO)
		haversine_dict[name] = h_dist
	sorted_cities = sorted(haversine_dict.items(), key=lambda x: x[1])
	sorted_list = []
	for value in sorted_cities:
		sorted_list.append(value[0])
	return sorted_list


if __name__ == '__main__':
	main()