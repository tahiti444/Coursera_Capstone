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


# Functions:
#################################################################
# function to avoid generating testing variables of json indenxed files (only for test):
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

# function to pass a link and get a request and a json data out of it
def get_df(link):
    results = requests.get(link).json()
    # print (results)
    # Pretty printing:
    json_string = json.dumps(results, sort_keys=True, indent=2)
    # print(json_string)
    # generate a python variable to access data:
    jdata = json.loads(json_string)
    jdata = jdata['response']['venues']
    # jdata = jdata['response']['groups']
    # view_json(jdata)              # object of a self-made function which prints json beautified!
    # lets import this data into pandas
    dataframe = json_normalize(jdata)
    # print (df.columns)
    # print (df.head())
    return dataframe

# keep only columns that include venue name, and anything that is associated with location
def filter_df(dataframe):
    filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
    dataframe = dataframe.loc[:, filtered_columns]  
    dataframe = dataframe.rename(columns=lambda x: re.sub('location.','',x))
    return dataframe


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

# Get a DataFrame from the mean position of boroughs in Toronto:
#################################################################
'''
Procedure:

    - try to group positions from geo_df for every Borough
    - find the mean lat and lng from each
    - do a search from every Borough
'''
u_list = {
    'Borough': '',
    'Latitude': 0.0,
    'Longitude': 0.0
}
boroughs_mean_pos = pd.DataFrame(columns=u_list)
for borough in geo_df['Borough'].unique():
    df_inter = geo_df[(geo_df['Borough']==borough)]
    # u_list = (x, y, z) x=borough, y=latitude, z=longitude
    x=borough
    y=df_inter['Latitude'].mean()
    z=df_inter['Longitude'].mean()
    u_list = {
        'Borough': x,
        'Latitude': y,
        'Longitude': z
    }
    u_list = pd.Series(u_list)
    boroughs_mean_pos = boroughs_mean_pos.append(u_list, ignore_index=True)

# print (boroughs_mean_pos)

# Make a request and convert it to json data
###############################################################
# locationTO = str(str(geo_df.iloc[0]['Latitude']) + ',' + str(geo_df.iloc[0]['Longitude']))
# lonTO = geo_df.iloc[0]['Longitude']
# latTO = geo_df.iloc[0]['Latitude']
# latTO = 43.727        # --> Real Center
# lonTO = -79.373       # --> Real Center
latTO = 43.6813         # --> Old city Center
lonTO = -79.4003        # --> Old city Center
locationTO = str(str(latTO) + ',' + str(lonTO))


coffeeTO = Link(option='search', location=locationTO, query='coffee').venue(radius=5000,limit=80) # radius in meters?
libraryTO = Link(option='search', location=locationTO, query='library').venue(radius=5000,limit=80) # radius in meters?
studyTO = Link(option='search', location=locationTO, query='study').venue(radius=5000,limit=80) # radius in meters?

df_coffee = get_df(coffeeTO)
df_library = get_df(libraryTO)
df_study = get_df(studyTO)


# Pandas data preparing:
#################################################################
# keep only columns that include venue name, and anything that is associated with location
df_coffee = filter_df(df_coffee)
df_library = filter_df(df_library)
df_study = filter_df(df_study)

# filter the category for each row
df_coffee['categories'] = df_coffee.apply(get_category_type, axis=1)
df_library['categories'] = df_library.apply(get_category_type, axis=1)
df_study['categories'] = df_study.apply(get_category_type, axis=1)

# generate map centered on the middle of Toronto:
#################################################################
mapTO = folium.Map(location=[latTO, lonTO], zoom_start=12)

# instantiate a feature group for the incidents in the dataframe
coffees = folium.map.FeatureGroup()
libraries = folium.map.FeatureGroup()
studies = folium.map.FeatureGroup()

# loop through the coffees
for latitude, longitude, in zip(df_coffee.lat, df_coffee.lng):
    coffees.add_child(
        folium.CircleMarker(
            [latitude, longitude],
            radius=5, # define how big you want the circle markers to be
            color='black',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )
# loop through the libraries
for latitude, longitude, in zip(df_library.lat, df_library.lng):
    libraries.add_child(
        folium.CircleMarker(
            [latitude, longitude],
            radius=5, # define how big you want the circle markers to be
            color='black',
            fill=True,
            fill_color='red',
            fill_opacity=0.6
        )
    )
# loop through the studies
for latitude, longitude, in zip(df_study.lat, df_study.lng):
    studies.add_child(
        folium.CircleMarker(
            [latitude, longitude],
            radius=5, # define how big you want the circle markers to be
            color='black',
            fill=True,
            fill_color='green',
            fill_opacity=0.6
        )
    )

mapTO.add_child(coffees)
mapTO.add_child(libraries)
mapTO.add_child(studies)
mapTO.save('index.html')











