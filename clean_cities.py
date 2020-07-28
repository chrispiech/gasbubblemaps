from SimpleTable import SimpleTable

def main():
	table = SimpleTable('data/us_cities.csv')
	ca_table = clean(table)
	ca_table.save('data/us_cities_clean.csv')

def clean(table):
	ca_table = SimpleTable()
	ca_table.set_col_names(['Name', 'Coords'])
	for city in table:
		name = city['city']
		state = city['state_name']
		state_id = city['state_id']
		lat = city['lat']
		lon = city['lng']
		ca_table.add_row({
			'Name':name + ' '+ state_id,
			'Coords':lon + ',' + lat
		})
	return ca_table


if __name__ == '__main__':
	main()