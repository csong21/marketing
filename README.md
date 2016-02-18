# marketing

1. geocoding.py is written to transform the addresses of all NYC WeWork locations into coordinates;

2. yelp_api_search_business.py is written to query for local businesses within a radius around all NYC WeWork locations, using lat/lon information generated by geocoding.py. It first uses yelp's search api, then uses its business api to query additional information about the top result from the search query.

3. Demographic and profile data at the neighborhood level is downloaded from the Open Data Portal NYC at https://data.cityofnewyork.us/City-Government/Demographics-and-profiles-at-the-Neighborhood-Tabu/hyuz-tij8

4. An interactive map on ESRI's customer tapestry segmentation: http://arcg.is/1PGND5y
5. A heatmap of Twitter feeds with hashtag #coworking, hosted on CartoDB is here:
https://ceceliasong.cartodb.com/viz/7d326a42-d5a5-11e5-8699-0ecfd53eb7d3/public_map
