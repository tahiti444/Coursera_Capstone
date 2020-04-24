# Main Program
''' 
Retrieving data from foursquare's API:
    - https://api.foursquare.com/V2/venues
                                    /users
                                    /tips
    - needs to pass:
        + Class Link
    - Read from external json file API_ID_Keys
    - Exercise: Load data from Neighborhoods and mathing them with postal codes
    - Request to FS API about:
        + Coffee
        + Library
        + study
        + party (optional)
    - transform request into json format
    - generatation of a map

    TODO: Build a cluster
'''

from pathlib import Path

# working with json and tranforming json file into a pandas dataframe library
import json
from pandas.io.json import json_normalize

import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
import folium # plotting library

# regex
import re

# Get credentials from json file
#########################################################################
wksPath = Path(__file__).parents[0]
# Open json file and return content of it
def readFile(nameFile):
    path = wksPath /  nameFile
    with open(path, 'r') as file:
        content = file.read()
        return content


# Globals initialization
#########################################################################
# read json file and save it
id_key = readFile('credentials.json')
id_key = json.loads(id_key)
# inizializate id credentials
client_id = id_key["client_id"]
client_secret = id_key["client_secret"]
version = str(20180602)
# object for URL from foursquare's API
main_URL = 'https://api.foursquare.com/v2/'


# TODO: missing functions: Link.user() and Link.tip()...
# TODO: explore, trending in option
# Classes---
##########################################################################
'''
class Link() -> generates a link to query the json file out of foursquare's API:
    method url_from_venue -> generates this link for venues and needs of: 
        option,         venues
        location,       as: latitud, longitud
        query           as: coffee, chinese food, windsurf...
'''
class Link:

    global main_URL, client_id, client_secret, version

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def venue(self, **kwargs):
        self.option = '/' + self.option + '?'
        self.location = 'll=' + self.location
        self.query = '&query=' + self.query
        url = str(main_URL+'venues'+self.option+self.location+self.query+'&client_id='+client_id+'&client_secret='+client_secret+'&v='+version)
        # kwargs should have the same name as in Foursquare
        for key, value in kwargs.items():
            append = '&' + key + '=' + str(value)
            url = url + append
        return (url)

    # TODO: Finish it...
    def explore(self):
        self.option = '/' + self.option + '?'
        self.location = 'll=' + self.location
        self.query = '&query=' + self.query
        url = str(main_URL+'venues'+self.option+self.location+self.query+'&client_id='+client_id+'&client_secret='+client_secret+'&v='+version)
        return (url)


# function to avoid generating testing variables:
def view_json(var):
    var = json.dumps(var, sort_keys=True, indent=2)
    return print (var)

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']


# Examples of queries:
#################################################################
# Search example
# coffeeNY = Link(option='search', location='40.7,-74', query='coffee').venue()
# print(coffeeNY)

# explore example
# exploreNY = Link(option='explore', location='40.7,-74', query='coffee').explore()
# print(exploreNY)

# FIXME: trending example
# trendingNY = Link(option='trending', location='40.7,-74', query='coffee').venue()
# print(trendingNY)


# Request and view information from url
###############################################################
'''
Import data of Toronto, clean it and assign it to postal codes for later continue with clustering
'''

url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

# Let's import, clear and rename the data frame
series_of_dataframes = pd.read_html(url)    # import raw data
df_first = series_of_dataframes[0]          # first dataframe from sereies of dataframes

# Select not assigned (na)
# na_nan_series = (df_first['Borough']=='Not assigned') & (df_first['Neighborhood'].isnull())
na_series = df_first['Borough']=='Not assigned'

# define clear of na's dataframe
df = df_first[na_series==False].rename(columns={'Postal code': 'PostalCode'})
# print (df.head())

# let's continue and separate them with comma as asked
df['Neighborhood'] = df['Neighborhood'].str.replace('/', ',')
# print ('Dataframe now comma-separated\n', df.head())

# !cat ../data/Geospatial_Coordinates.csv
geo_df = pd.read_csv('./data/Geospatial_Coordinates.csv')
geo_df = geo_df.rename(columns={'Postal Code': 'PostalCode'})

geo_df = df.merge(geo_df, how='outer', on='PostalCode')
# print (geo_df)


# Make a request and convert it to json data
###############################################################
locationTO = str(str(geo_df.iloc[0]['Latitude']) + ',' + str(geo_df.iloc[0]['Longitude']))
lonTO = geo_df.iloc[0]['Longitude']
latTO = geo_df.iloc[0]['Latitude']
# lonTO = 43.727        # --> Real Center
# latTO = -79.373       # --> Real Center

sportTO = Link(option='search', location=locationTO, query='Gym').venue(limit=80)
# print (sportTO)

# results = requests.get(url).json()
results = requests.get(sportTO).json()
# print (results)

# Pretty printing:
json_string = json.dumps(results, sort_keys=True, indent=2)
# print (json_string)

# generate a python variable to access data:
jdata = json.loads(json_string)
# print (type(jdata))           # -> dictionary

jdata = jdata['response']['venues']
# view_json(jdata)              # object of a self-made function which prints json beautified!

# lets import this data into pandas
df = json_normalize(jdata)
# print (df.columns)
# print (df.head())

# Import from API up to 80 venues about sport in Toronto
###############################################################
'''
Info about Foursquare Sand Box Account:
    - The Foursquare API has a limit of:
        + 950 Regular API Calls per day and 
        + 50 Premium API Calls per day for Sandbox Tier Accounts.

Example: (more info: https://developer.foursquare.com/docs/places-api/getting-started/)

import json, requests
url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
    client_id='CLIENT_ID',
    client_secret='CLIENT_SECRET',
    v='20180323',
    ll='40.7243,-74.0018',
    query='coffee',
    limit=1
    )

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)
'''

# Pandas data preparing:
#################################################################
# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in df.columns if col.startswith('location.')] + ['id']
df_filtered = df.loc[:, filtered_columns]

# rename_columns, whitout 'location.'
df_filtered = df_filtered.rename(columns=lambda x: re.sub('location.','',x))

# filter the category for each row
df_filtered['categories'] = df_filtered.apply(get_category_type, axis=1)

# Coordinates for map centering:
#################################################################
# FIXME: Problem with folium... lets itself not force to some manually tipped location inputs

# latTO = 43.727
# lonTO = -79.373
for lat in df_filtered['lat']:
    if (43.729 > lat > 43.726):
        latcenterTo = lat
        break
    else:
        pass

for lng in df_filtered['lng']:
    if -79.374 < lng < -79.371:
        lngcenterTo = lng
        break

# generate map centered on the middle of Toronto:
#################################################################
# mapTO = folium.Map(location=[latTO, lonTO], zoom_start=13)
mapTO = folium.Map(location=[latcenterTo, lngcenterTo], zoom_start=12)
mapTO.save('index.html')






# Section_Sample
###############################################################