import requests
import json
import polyline
from SimpleTable import SimpleTable

"""
Rate limits:
Elevation linestrings (2.000 requests per day @40 requests per minute)
Directions (2.000 requests per day @40 requests per minute)
40/min means you should pause >= 1.5s between requests

https://api.openrouteservice.org/v2/directions/driving-car?api_key=5b3ce3597851110001cf6248b44db44b33c64508afa658b8673c9580&start=8.681495,49.41461&end=8.687872,49.420318
"""
DIR_URL = 'https://api.openrouteservice.org/v2/directions/cycling-road'
ELEVATION_URL = 'https://api.openrouteservice.org/elevation/line'

API_KEY = '5b3ce3597851110001cf6248b44db44b33c64508afa658b8673c9580'

def main():
	data = SimpleTable('uscities.csv')
	print(data)
	# palo_alto = '-122.161760,37.449925',
	# san_francisco = '-122.414971,37.753623'
	# route = get_route(palo_alto, san_francisco)
	# elevation_route = get_route_elevation(route)
	# validate_elevation(elevation_route)

def validate_elevation(route_with_elevation):
	for point in route_with_elevation:
		elevation = point[2]
		print(elevation)

def get_route_elevation(route):
	encoded_route = polyline.encode(route,geojson=True)
	body = {
		"format_in":"encodedpolyline",
		"geometry":encoded_route
	}

	headers = {
	    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
	    'Authorization': API_KEY,
	    'Content-Type': 'application/json; charset=utf-8'
	}
	call = requests.post('https://api.openrouteservice.org/elevation/line', json=body, headers=headers)
	return json.loads(call.text)['geometry']['coordinates']

def get_route(gps_a, gps_b):
	params = {
		'api_key':API_KEY,
		'start':gps_a,
		'end':gps_b
	}
	call = requests.get(DIR_URL, params)
	return json.loads(call.text)['features'][0]['geometry']['coordinates']

if __name__ == '__main__':
	main()