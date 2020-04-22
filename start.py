# Main Program
''' 
Retrieving data from foursquare's API:
    - https://api.foursquare.com/V2/venues
                                    /users
                                    /tips
    - needs to pass:
        + ID
        + Secret ID
        + Version (usufull for controling your app)

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


# TODO: missing url_from_users and url_from_tips...
# TODO: explore, trending in option
# Classes
##########################################################################
'''
class Link() -> generates a link to query the json file out of foursquare's API:
    method url_from_venue -> generates this link for venues and needs of: 
        option,         venues
        location,       as: latitud, longitud
        query           as: coffee, chinese food, windsurf...

examples:
    Specific venue category:
    + venues/ + option + ? + client_id= + CLIENT_ID + &client_secret= + CLIENT_SECRET + &ll= + LOCATION + &query= + QUERY + &radius= + RADIUS + &limit=  + LIMIT
    - 'https://api.foursquare.com/v2/venues/search?client_id=P1YQAFRAQSNTLIX1ZSRRLUDXB2JGT0KPNSPGFBWXOMBVL4X4&client_secret=HEADURYPNTU24PWKRJADVLS5OMSOU0XKKN4H5F4E5YYFUZJ1&ll=40.7149555,-74.0153365&v=20180604&query=Italian&radius=500&limit=30'

    Explore a given venue:
    + venues/ + ID + ? + client_id= + CLIENT_ID + &client_secret= + CLIENT_SECRET 
    - 'https://api.foursquare.com/v2/venues/4fa862b3e4b0ebff2f749f06?client_id=P1YQAFRAQSNTLIX1ZSRRLUDXB2JGT0KPNSPGFBWXOMBVL4X4&client_secret=HEADURYPNTU24PWKRJADVLS5OMSOU0XKKN4H5F4E5YYFUZJ1&v=20180604'

    Get the venue tips:
    + venues/ + ID + tips + ? + CLIENT_ID + &client_secret= + CLIENT_SECRET
    - https://api.foursquare.com/v2/venues/VENUE_ID/tips?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=VERSION&limit=LIMIT

    Search a user:
    + users/ + ID + ? + CLIENT_ID + &client_secret= + CLIENT_SECRET
    - https://api.foursquare.com/v2/users/USER_ID?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=VERSION

    Search tips from a given user:
    + users/ + ID + /tips + ? + client_id= + CLIENT_ID + &client_secret= + CLIENT_SECRET + &v= + VERSION + &limit= + LIMIT
    - https://api.foursquare.com/v2/users/{}/tips?client_id={}&client_secret={}&v={}&limit={}'.format(user_id, CLIENT_ID, CLIENT_SECRET, VERSION, limit)
'''
class Link:

    global main_URL, client_id, client_secret, version

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def venue(self):
        self.option = '/' + self.option + '?'
        self.location = 'll=' + self.location
        self.query = '&query=' + self.query
        url = str(main_URL+'venues'+self.option+self.location+self.query+'&client_id='+client_id+'&client_secret='+client_secret+'&v='+version)
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



# Search example
coffeeNY = Link(option='search', location='40.7,-74', query='coffee').venue()
# print(coffeeNY)

# explore example
exploreNY = Link(option='explore', location='40.7,-74', query='coffee').explore()
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


# Test data from request
###############################################################

# print (geo_df.iloc[0])
'''
PostalCode             M3A
Borough         North York
Neighborhood     Parkwoods
Latitude           43.7533
Longitude         -79.3297
Name: 0, dtype: object
'''
location1 = str(str(geo_df.iloc[0]['Latitude']) + ',' + str(geo_df.iloc[0]['Longitude']))
# print (location1)

# sportTO = Link(option='search', location=location1, query='sport').venue()
sportTO = Link(option='search', location=location1, query='Gym').venue()
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



# TestData
###############################################################
jdata = jdata['response']['venues']
# view_json(jdata)              # object of a self-made function which prints json beautified!

# lets import this data into pandas
df = json_normalize(jdata)
# print (df.columns)
# print (df.head())

# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in df.columns if col.startswith('location.')] + ['id']
df_filtered = df.loc[:, filtered_columns]

# rename_columns, whitout 'location.'
df_filtered = df_filtered.rename(columns=lambda x: re.sub('location.','',x))

# filter the category for each row
df_filtered['categories'] = df_filtered.apply(get_category_type, axis=1)
print (df_filtered.columns)
print (df_filtered.shape)
print (df_filtered.head(50))



# Section_Sample
###############################################################