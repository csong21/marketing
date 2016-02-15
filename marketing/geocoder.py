import json
import requests
import numpy

APIKEY = '64557a79af970d7ec545e8f7f36797c9b73c15d2'
APIURL = 'https://ceceliasong.cartodb.com/api/v2/sql'

def geocoder(locat_table):
	query = """SELECT name, cdb_geocode_street_point(address) 
			AS the_geom FROM %s"""%(locat_table)
	r = requests.get(APIURL, params=dict(api_key=APIKEY, q=query,format='geojson'))
	data = r.json()['features']
	return data

def parse(data, update, locat_table):
	locations=[]
	for i in data:
		location = []
		name = i['properties']['name']
		lon = i['geometry']['coordinates'][0]
		lat = i['geometry']['coordinates'][1]
		location = [name,lon,lat]
		if update is True:
			print 'table updated'
			update_table(locat_table, lon,lat,name)
		locations.append(location)
	return locations

def update_table(table, lon_field, lat_field, name):
	query = """
			UPDATE %s 
			SET lon = %f, lat = %f
			WHERE name = '%s';
			""" % (table, lon_field, lat_field, name)
	r = requests.get(APIURL, params=dict(api_key=APIKEY, q=query))

def main():
	locat_table = 'wework_locations_nyc'
	#data = geocoder(locat_table) #run once to get the coordinates
	"""hold the results:"""
	data = [{u'geometry': {u'type': u'Point', u'coordinates': [-73.99129, 40.69435]}, u'type': u'Feature', u'properties': {u'name': u'Brooklyn Heights'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.92497, 40.75501]}, u'type': u'Feature', u'properties': {u'name': u'Studio Square'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98748, 40.70089]}, u'type': u'Feature', u'properties': {u'name': u'Dumbo Heights'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98642, 40.75506]}, u'type': u'Feature', u'properties': {u'name': u'Time Square'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98811, 40.73511]}, u'type': u'Feature', u'properties': {u'name': u'Irving Place'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.01143, 40.70395]}, u'type': u'Feature', u'properties': {u'name': u'FiDi'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00652, 40.70478]}, u'type': u'Feature', u'properties': {u'name': u'Wall Street'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.983498, 40.75016]}, u'type': u'Feature', u'properties': {u'name': u'5th Ave'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.009059, 40.710161]}, u'type': u'Feature', u'properties': {u'name': u'John Street'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98543, 40.74415]}, u'type': u'Feature', u'properties': {u'name': u'NoMad'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00139, 40.71976]}, u'type': u'Feature', u'properties': {u'name': u'SoHo South'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.01381, 40.70545]}, u'type': u'Feature', u'properties': {u'name': u'Charging Bull'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.99342, 40.75397]}, u'type': u'Feature', u'properties': {u'name': u'Penn Station'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00876, 40.71101]}, u'type': u'Feature', u'properties': {u'name': u'Fulton Center'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.959823, 40.716068]}, u'type': u'Feature', u'properties': {u'name': u'Williamsburg'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.9738, 40.75067]}, u'type': u'Feature', u'properties': {u'name': u'42nd Street'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00572, 40.72737]}, u'type': u'Feature', u'properties': {u'name': u'SoHo West'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98416, 40.75308]}, u'type': u'Feature', u'properties': {u'name': u'Bryant Park'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00247, 40.72372]}, u'type': u'Feature', u'properties': {u'name': u'West Broadway'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.995622, 40.740261]}, u'type': u'Feature', u'properties': {u'name': u'Chelsea'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.984, 40.74314]}, u'type': u'Feature', u'properties': {u'name': u'Park South'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98571, 40.73974]}, u'type': u'Feature', u'properties': {u'name': u'Gramercy'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.99881, 40.72006]}, u'type': u'Feature', u'properties': {u'name': u'Soho'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98076, 40.75054]}, u'type': u'Feature', u'properties': {u'name': u'Madison'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-73.98452, 40.74819]}, u'type': u'Feature', u'properties': {u'name': u'Empire State'}}, {u'geometry': {u'type': u'Point', u'coordinates': [-74.00671, 40.73968]}, u'type': u'Feature', u'properties': {u'name': u'Meatpacking'}}]
	locations = parse(data, True, locat_table)
	print locations
	locations = [[u'Brooklyn Heights', -73.99129, 40.69435], [u'Studio Square', -73.92497, 40.75501], [u'Dumbo Heights', -73.98748, 40.70089], [u'Time Square', -73.98642, 40.75506], [u'Irving Place', -73.98811, 40.73511], [u'FiDi', -74.01143, 40.70395], [u'Wall Street', -74.00652, 40.70478], [u'5th Ave', -73.983498, 40.75016], [u'John Street', -74.009059, 40.710161], [u'NoMad', -73.98543, 40.74415], [u'SoHo South', -74.00139, 40.71976], [u'Charging Bull', -74.01381, 40.70545], [u'Penn Station', -73.99342, 40.75397], [u'Fulton Center', -74.00876, 40.71101], [u'Williamsburg', -73.959823, 40.716068], [u'42nd Street', -73.9738, 40.75067], [u'SoHo West', -74.00572, 40.72737], [u'Bryant Park', -73.98416, 40.75308], [u'West Broadway', -74.00247, 40.72372], [u'Chelsea', -73.995622, 40.740261], [u'Park South', -73.984, 40.74314], [u'Gramercy', -73.98571, 40.73974], [u'Soho', -73.99881, 40.72006], [u'Madison', -73.98076, 40.75054], [u'Empire State', -73.98452, 40.74819], [u'Meatpacking', -74.00671, 40.73968]]

if __name__ == '__main__':
	main()