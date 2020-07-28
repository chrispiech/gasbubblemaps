import requests
import json
import polyline
import pickle
from math import radians, cos, sin, asin, sqrt
import time

METERS_TO_FEET = 3.28084
PALO_ALTO = '-122.161760,37.449925'

ELEVATION_POINT_URL = 'https://api.openrouteservice.org/elevation/point'
DRIVING_URL = 'https://api.openrouteservice.org/v2/directions/driving-car'
BIKING_URL = 'https://api.openrouteservice.org/v2/directions/cycling-road'
DIRECTION_URL = DRIVING_URL
ELEVATION_URL = 'https://api.openrouteservice.org/elevation/line'
API_KEYS = [
    '5b3ce3597851110001cf6248b44db44b33c64508afa658b8673c9580',
    '5b3ce3597851110001cf624869c3108284684b1296925af9c19dea75',
    '5b3ce3597851110001cf62484bb226a4c1fa4cb1a3dda326760fba09'
]
API_KEY = API_KEYS[0]

"""
I use a cheeky global route_cache...
"""


def get_route_with_elevation(route_name, gps_a, gps_b):
    # first check the cache
    if route_cache and route_name in route_cache:
        value = route_cache[route_name]
        if value != None:
            return value
    route = _get_route_with_elevation_helper(gps_a, gps_b)
    time.sleep(1.5)
    if route == None:
        print('route not found')
    if route_cache != None:
        route_cache[route_name] = route
        save_route_cache()
    return route

def get_elevation_of_point(gps_point):
    params = {
        'api_key':API_KEY,
        'geometry':gps_point
    }
    call = requests.get(ELEVATION_POINT_URL, params)
    result = json.loads(call.text)
    if not 'geometry' in result:
        return None
    coord = result['geometry']['coordinates']
    return coord[2]
    
def _get_route_with_elevation_helper(gps_a, gps_b):
    """
    returns a list of points where each point is a list with
    lon, lat and altitude (in meters)
    """
    route = get_route(gps_a, gps_b)
    if route == None:
        return None
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
    result = json.loads(call.text)
    if not 'geometry' in result:
        print(result)
        return None
    return result['geometry']['coordinates']

def get_route(gps_a, gps_b):
    params = {
        'api_key':API_KEY,
        'start':gps_a,
        'end':gps_b
    }
    call = requests.get(DIRECTION_URL, params)
    result = json.loads(call.text)
    if not 'features' in result:
        print(result)
        return None
    return result['features'][0]['geometry']['coordinates']

def haversine(latlon1, latlon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) in kilometers
    """

    lat1,lon1 = split_lat_lon_str(latlon1)
    lat2,lon2 = split_lat_lon_str(latlon2)
    
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def split_lat_lon_str(latlon):
    parts = latlon.split(',')
    return float(parts[0]), float(parts[1])

def turn_on_cache(file_path):
    global cache_path, route_cache
    cache_path = file_path
    route_cache = load_route_cache()

def load_route_cache():
    try:
        return pickle.load(open(cache_path, 'rb'))
    except:
        return {}

def save_route_cache():
    pickle.dump(route_cache, open(cache_path, 'wb'))

cache_path = None
route_cache = None
