us_route_distances.ipynb / us_route_distances.py

Description: Reads-in .xlsx file with pairs of 5-digit US zip code combinations and calculates 
(1) actual road miles and (2) the straight-line distance between the two points via Open-source 
Routing Machine (OSRM) API; similar to Google Maps.

INPUT (2 columns): 	Origin Zip, Destination Zip
OUTPUT (8 columns): 	Origin Zip, Destination Zip, Origin Latitude, Origin Longitude, 
				Destination Latitude, Destination Longitude, Straight-line Distance, 
				Road Miles

OSRM API Documentation: http://project-osrm.org/docs/v5.7.0/api/?language=Python#general-options