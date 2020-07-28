from SimpleTable import SimpleTable
from util import *

PATH = 'cache/city_elevations.pkl'

def main():
	explore()

def explore():
	ca_table_dict = SimpleTable('data/ca_cities.csv').to_dict('Name')

	ca_low = SimpleTable()
	ca_low.set_col_names(['Name', 'Coords', 'Elevation'])
	elevation_map = pickle.load(open(PATH, 'rb'))
	for city_name in elevation_map:
		elevation = elevation_map[city_name]
		if elevation != None:
			elevation_ft = elevation * METERS_TO_FEET
			if elevation_ft <= 1000:
				coords = ca_table_dict[city_name]['Coords']
				ca_low.add_row({
					'Name':city_name,
					'Elevation':elevation_ft,
					'Coords':coords
				})
	ca_low.save('data/ca_low.csv')

def generate():
	ca_table = SimpleTable('data/ca_cities.csv')
	city_elevations = {}
	n_done = 0
	for city in ca_table:
		name = city['Name']
		gps = city['Coords']
		elevation = get_elevation_of_point(gps)
		city_elevations[name] = elevation
		if n_done % 100 == 0:	
			pickle.dump(city_elevations, open(PATH, 'wb'))
		n_done += 1
		print(n_done)

if __name__ == '__main__':
	main()