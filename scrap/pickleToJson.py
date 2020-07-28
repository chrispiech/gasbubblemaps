import pickle
import json
from util import *

def main():
	data = pickle.load(open('cache/nearBay.pkl', 'rb'))
	json.dump(data, open('client/nearBay.json', 'w'))
	paths = []
	stop_points = []
	for key in data:
		route = data[key]
		if route == None: continue
		remaining = reduce_to_1000(route, stop_points)
		paths.append(remaining)
	json.dump(paths, open('client/paths.json', 'w'))
	json.dump(stop_points, open('client/stopPoints.json', 'w'))


def reduce_to_1000(route, stop_points):
	remaining = []
	for point in route:
		elevation = point[2] * METERS_TO_FEET
		if elevation >= 1500:
			stop_points.append(point)
			return remaining
		remaining.append(point)
	return remaining

if __name__ == '__main__':
	main()