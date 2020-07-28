import json
import geopandas as gpd
from shapely.geometry import  MultiLineString
from util import *
"""
list of nodes
each node has location, elevation and reference to an edge

list of edges
each edge has a path with elevations
"""

def main():
	all_highways = load_highway_data()
	elevation_map = {}

	edge_map = {}
	
	for road in all_highways:
		for i in range(len(road) - 1):


			node =normalize_point(road[i])
			next_node = normalize_point(road[i+1])
			# keep track of all elevations
			elevation_map[node] = road[i][2]
			elevation_map[next_node] = road[i+1][2]

			if not node in edge_map:
				edge_map[node] = set([])
			if not next_node in edge_map:
				edge_map[next_node] = set([])

			edge_map[node].add(next_node)
			edge_map[next_node].add(node)

	for x in range(500, 3100, 100):
		print(x)
		dfs_paths = dfs(edge_map, elevation_map, x)
		file_name = 'data/dfs' + str(x) + '.json'
		json.dump(dfs_paths, open('client/' + file_name, 'w'))

def dfs(edge_map, elevation_map, max_elevation):
	start = (-122.16178, 37.44991)

	all_paths = []
	dfs_stack = [start]
	curr_path = []
	visited = set([])
	last_node = None
	parent_map = {}

	while len(dfs_stack) > 0:
		curr_node = dfs_stack.pop()
		elevation = elevation_map[curr_node]
		is_high = elevation >= (max_elevation / METERS_TO_FEET)
		is_new_path = last_node and curr_node not in edge_map[last_node]

		n_neighbors = len(edge_map[curr_node])
		# if n_neighbors > 2:
		# 	intersections.append(curr_node)

		# base case
		if curr_node in visited:
			continue
		visited.add(curr_node)
		if is_high:
			curr_path.append([
				curr_node[0],
				curr_node[1],
				elevation
			])
			curr_path = start_new_path(all_paths, curr_path, curr_node, parent_map, elevation_map)
			continue

		if is_new_path:
			curr_path = start_new_path(all_paths, curr_path, curr_node, parent_map, elevation_map)
			

		curr_path.append([
			curr_node[0],
			curr_node[1],
			elevation
		])

		# recurse
		for child in edge_map[curr_node]:
			parent_map[child] = curr_node
			dfs_stack.append(child)

		
		last_node = curr_node

	all_paths.append(curr_path)
	return all_paths

def start_new_path(all_paths, curr_path, curr_node, parent_map, elevation_map):
	all_paths.append(curr_path)
	curr_path = []

	parent_node = parent_map[curr_node]
	curr_path.append([
		parent_node[0],
		parent_node[1],
		elevation_map[parent_node]
	])
	return curr_path

def load_highway_data():
	all_paths = []
	roads = pickle.load(open('cache/nearBay.pkl', 'rb'))
	i = 0
	for key in roads:
		road = roads[key]
		if road != None:
			add_path(all_paths, road, i)
			i += 1

	return all_paths

def add_path(all_paths, points, name):
	path = []
	for point in points:
		path.append(point)
	path = tuple(path)
	all_paths.append(path)
	

def normalize_point(point):
	# precise to 1 meters
	lng = point[0]
	lat = point[1]
	return (lng, lat)

if __name__ == '__main__':
	main()