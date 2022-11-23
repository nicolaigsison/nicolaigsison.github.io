# Check Python Version Number
from platform import python_version
python_version()

# Imports
import pandas as pd
import numpy as np
import requests
import folium
import polyline
import osrm
import aiohttp
import pgeocode
from geopy.distance import great_circle
from pyzipcode import ZipCodeDatabase
nomi = pgeocode.Nominatim('US')

# Installations
# %pip install GDAL-3.4.3-cp38-cp38-win_amd64.whl
# %pip install --upgrade git+https://github.com/ustroetz/python-osrm.git 
# https://githubmemory.com/repo/ustroetz/python-osrm/issues/40 # Debugging
# print(osrm.__file__) # filepath

class US_Route_Distances:
    # Read in data as pandas DataFrame
    def __init__(self, filepath, filename):
        self.df = pd.read_excel(filepath + '\\' + filename + '.xlsx', dtype=str)
    
    # Adds latitude and longitude coordinates to each O-D pair combination via zip code query
    def lat_long(self, zip_cols, coord_cols):
        orig_lat, orig_long, dest_lat, dest_long = [], [], [], []
        for index, value in self.df.iterrows():
            orig_lat.append(nomi.query_postal_code(self.df[zip_cols[0]][index])[9])
            orig_long.append(nomi.query_postal_code(self.df[zip_cols[0]][index])[10])
            dest_lat.append(nomi.query_postal_code(self.df[zip_cols[1]][index])[9])
            dest_long.append(nomi.query_postal_code(self.df[zip_cols[1]][index])[10])
        self.df[coord_cols[0]], self.df[coord_cols[1]], self.df[coord_cols[2]], self.df[coord_cols[3]] = orig_lat, orig_long, dest_lat, dest_long
        self.df.dropna(how='any', inplace=True)
        return self.df
    
    # Adds straight-line distance (pygeocode) and actual road miles (OSRM) via lat/long coordinates
    def us_distances(self, coord_cols):
        road_miles, straightline_dist = [], []
        for index, value in self.df.iterrows():
            origin_lat, origin_long, dest_lat, dest_long = self.df[coord_cols[0]][index], self.df[coord_cols[1]][index], self.df[coord_cols[2]][index], self.df[coord_cols[3]][index]
            url = "http://router.project-osrm.org/route/v1/driving/" + str(origin_long) + "," + str(origin_lat) + ";" + str(dest_long) + "," + str(dest_lat) + '?overview=false'
            r = requests.get(url)
            res = r.json()
            if res['code'] == 'Ok':
                road_miles.append(round(res['routes'][0]['distance']/1609.344, 2))
            else: road_miles.append(res['code'])
            straightline_dist.append(round(great_circle((origin_lat, origin_long), (dest_lat, dest_long)).miles, 2))
        self.df["Straight-Line Distance"], self.df["Road Miles"] = straightline_dist, road_miles
        return self.df

    # Export results to .xlsx file
    def get_results(self, filepath, filename):
        self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        self.df.to_excel(filepath + '\\' + filename + '.xlsx', index=False)

# Run US_Route_Distances class
filepath = r'filepath'
zip_cols, coord_cols = ['Origin Zip', 'Destination Zip'], ['Origin Latitude', 'Origin Longitude', 'Destination Latitude', 'Destination Longitude']
test = US_Route_Distances(filepath, 'input_filename')
test.lat_long(zip_cols, coord_cols)
test.us_distances(coord_cols)
test.get_results(filepath, 'output_filename')
