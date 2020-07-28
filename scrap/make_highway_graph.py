import json
import geopandas as gpd
from shapely.geometry import  MultiLineString

"""
list of nodes
each node has location, elevation and reference to an edge

list of edges
each edge has a path with elevations
"""


def main():
	all_highways = load_highway_data()
	print(len(all_highways))
	intersections = find_intersections(all_highways)
	print(len(intersections))
	json.dump(intersections, open('client/intersections.json', 'w'))

def load_highway_data():
	all_paths = {}
	roads = gpd.read_file('data/ca_roads/roads.shp')
	for index, row in roads.iterrows():
		name = row['FULLNAME']
		geometry = row['geometry']
		if isinstance(geometry, MultiLineString):
			for single_line in geometry.geoms:
				add_path(all_paths, single_line, name)
		else:
			add_path(all_paths, geometry, name)
	return all_paths

def add_path(all_paths, line_string, name):
	path = []
	for point in line_string.coords:
		path.append(point)
	all_paths[tuple(path)] = name
	
def find_intersections(all_highways):
	intersections = set([])
	location_cache = {}
	for road in all_highways:
		name = all_highways[road]
		for point in road:
			point = normalize_point(point)
			if point not in location_cache:
				location_cache[point] = set()
			location_cache[point].add(name)


	for road in all_highways:
		for j in range(len(road)-1):
			point = normalize_point(road[j])
			next_point = normalize_point(road[j+1])
			point = (point)
			n_points = len(location_cache[point])
			next_n_points = len(location_cache[next_point])
			if n_points > next_n_points and n_points >= 3:
				intersections.add(point)
			if next_n_points > n_points and next_n_points >= 3:
				intersections.add(next_point)
	
	return list(intersections)

def normalize_point(point):
	# precise to 1 meters
	lng = round(point[0], 5)
	lat = round(point[1], 5)
	return (lng, lat)

if __name__ == '__main__':
	main()