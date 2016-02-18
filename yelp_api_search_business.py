""
This script uses Yelp search API (version 2.0) to
query for local businesses within a radius around a WeWork location,
and then uses the Business API to query additional information about the top result
from the search query.

Future use sample:
yelp_api_search_business.py --term="professional service" --location="New York, New York"
"""
import argparse
import csv
import json
import pprint
import sys
import urllib
import urllib2
import oauth2

API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'professional service'
ALL_LOCATIONS = [[u'Brooklyn Heights', -73.99129, 40.69435], [u'Studio Square', -73.92497, 40.75501], [u'Dumbo Heights', -73.98748, 40.70089], [u'Time Square', -73.98642, 40.75506], [u'Irving Place', -73.98811, 40.73511], [u'FiDi', -74.01143, 40.70395], [u'Wall Street', -74.00652, 40.70478], [u'5th Ave', -73.983498, 40.75016], [u'John Street', -74.009059, 40.710161], [u'NoMad', -73.98543, 40.74415], [u'SoHo South', -74.00139, 40.71976], [u'Charging Bull', -74.01381, 40.70545], [u'Penn Station', -73.99342, 40.75397], [u'Fulton Center', -74.00876, 40.71101], [u'Williamsburg', -73.959823, 40.716068], [u'42nd Street', -73.9738, 40.75067], [u'SoHo West', -74.00572, 40.72737], [u'Bryant Park', -73.98416, 40.75308], [u'West Broadway', -74.00247, 40.72372], [u'Chelsea', -73.995622, 40.740261], [u'Park South', -73.984, 40.74314], [u'Gramercy', -73.98571, 40.73974], [u'Soho', -73.99881, 40.72006], [u'Madison', -73.98076, 40.75054], [u'Empire State', -73.98452, 40.74819], [u'Meatpacking', -74.00671, 40.73968]]

"""
DEFAULT_LOCATION = 'DUMBO, NY'
DEFAULT_CLL='40.700870,-73.987483'
"""
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credentials.
CONSUMER_KEY = '3EjacDLNytbicGCAIlri7g'
CONSUMER_SECRET = 'XVBwj667CqaEqZsfanyIWE6ZL2E'
TOKEN = 'x7OfQzIJpo26RkjHQ7Ayn60oV8ZdeyYu'
TOKEN_SECRET = 'zMTFOBd5m5BCsLnyfA72sGcD2XY'


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(
        method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(
        oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    #print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response


def search(term, location, cll, radius_filter):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'cll': cll,
        'limit': SEARCH_LIMIT,
        'radius_filter': radius_filter
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)


def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)


def query_api(location, term, cll, radius_filter):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location, cll, radius_filter)

    businesses = response.get('businesses')

    if not businesses:
        print u'No businesses for {0} in {1} found.'.format(term, location)
        return

    for b in businesses:
        b_name = b['name']
        b_locat = b['location']
        

        if 'categories' in b.keys():
            b_type = b['categories']
        else: 
            b_type = 'categories not indicated'


        #if neighborhoods in b['location'].keys():
         #   b_neighborhood = b['location']['neighborhoods']
        #else:
        #    b_neighborhood = 'neighborhood not indicated'

        #print b_type
        #print b_name
        #print b_locat
        print b_type
        print '\n'

    """

    business_id = businesses[0]['id']

    print u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id)
    response = get_business(business_id)

    print u'Result for business "{0}" found:'.format(business_id)
    pprint.pprint(response, indent=2)"""


def main():
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-c', '--cll', dest='cll',
                        default=DEFAULT_CLL, type=str,
                        help='Search cll (default: %(default)s)')

    input_values = parser.parse_args()
    try:

        query_api(input_values.term, input_values.location, input_values.cll)
    except urllib2.HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0}. Abort program.'.format(error.code))"""

    for location in ALL_LOCATIONS:
        name = location[0]
        where = '%s, New York, NY'%name
        print where
        #format for search api is: cll=latitude,longitude; e.g: cll='40.700870,-73.987483'
        cll = '%s,%s'%(location[2],location[1])
        print cll
        radius_filter = 1000 #set search radius to 1000m, proxy 10 blocks
        term = 'Professional Services'

        try:
            query_api(where, term, cll, radius_filter)
        except urllib2.HTTPError as error:
            sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))


if __name__ == '__main__':
    main()
