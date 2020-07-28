import pickle

from util import *

def main():
	data = pickle.load(open('cache/driving.pkl', 'rb'))
	for key in data:
		goal = key.split(',')[1]
		path = data[key]
		if path:
			is_safe = check_max_elevation(path)
			print(goal, is_safe)

def check_max_elevation(path):
	for point in path:
		elevation_meters = point[2]
		elevation_feet = elevation_meters * METERS_TO_FEET
		if elevation_feet >= 1000:
			return False
	return True

if __name__ == '__main__':
	main()