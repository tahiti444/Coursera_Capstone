# Main Program 
# 29.04.20 DGM:         Program's opening

''' 
ATTENTION to use this program:
    - you might want to overwrite in Globals Initialization:
        + client_id = <your ID>
        + client_secret = <your ID Key>
        YOU CAN ALSO: create a json file named: 'credentials.json' on the same folder and write:
        {
            'client_id': <your ID>,
            'client_secret': '<your ID Key>
        }
    - you may also want to actualize the cities DataFrame and uncomment the rows at the very beginning of this program

GOAL: 
    - Retrieve the actual companies' locations and plot them to a map to find out which companies about your sector in your surroundings you have, 
    in which city you should move to for this, etc. Feel free to change these queries and places to match your needs.

##################
PROCEDURE
##################
Retrieving data from foursquare's API:
    - needs to pass:
        + Class Link
    - Read from external json Foursquare API:
        + Load data from cities in Germany and matching them with queries
    - Request to FouSquare API about:
        + Data Science
        + Data Mining
        + Data Analysis
    - generatation of a map
##################
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

'''
Uncomment if want to actualize cities
'''

# url = 'https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population'

# series_df = pd.read_html(url, encoding='utf_16')
# # series_df = pd.read_html(url)
# df = series_df[0]
# df = df.drop(labels={'2015rank', '2015estimate', 'Change', '2011census', '2015land area', '2015populationdensity'}, axis=1)

# location_columns = df['Location'].str.split(pat="/", expand=True).rename(columns={0: 'cardLocation', 1: 'dLocation'})
# location_columns2 = location_columns['dLocation'].str.split(pat="°N", expand=True)
# location_columns2 = location_columns2.rename(columns={0: 'Latitude', 1: 'Longitude'})

# try:
#     location_columns2['Latitude'] = location_columns2['Latitude'].astype(float)
#     print ('converted to float')
# except Exception as e:
#     print (e)
#     print ('Trying to decode...')
#     location_columns2['Latitude'] = location_columns2['Latitude'].str.replace(u' \ufeff', u'')
#     location_columns2['Latitude'] = location_columns2['Latitude'].astype(float)
#     print('final data type from {} is {}'.format(location_columns2['Latitude'].name, location_columns2['Latitude'].dtypes))

# try:
#     location_columns2['Longitude'] = location_columns2['Longitude'].astype(float)
#     print ('converted to float')
# except Exception as e:
#     print (e)
#     print ('Trying to decode...')
#     location_columns2['Longitude'] = location_columns2['Longitude'].str.replace(u' \ufeff', u'')
#     location_columns2['Longitude'] = location_columns2['Longitude'].str.replace(u'°E', u'')
#     location_columns2['Longitude'] = location_columns2['Longitude'].astype(float)
#     print('final data type from {} is {}'.format(location_columns2['Longitude'].name, location_columns2['Longitude'].dtypes))

# df = pd.concat([df, location_columns2], axis=1)
# df = df.drop(labels={'Location'}, axis=1)

# position = pd.DataFrame(columns={'Position'})
# my_dict = {
#     'Position': ''
# }
# for idx in df.index:
#     string = str(round(df['Latitude'].iloc[idx], ndigits=3)) + ',' + str(round(df['Longitude'].iloc[idx], ndigits=3))
#     my_dict = {
#         'Position': string
#     }
#     position = position.append(my_dict, ignore_index=True)

# df = pd.concat([df, position], axis=1)

# df.to_csv('./data/loc_cities_germany.csv')

'''
Commented out after saving dataframe!
'''

# Find geocenter of Germany
geolocator = Nominatim(user_agent='aiFinder')
location = geolocator.geocode('Germany')

latGE = location.latitude           # --> Center
lonGE = location.longitude          # --> Center
locationGE = str(str(latGE) + ',' + str(lonGE))

# generate map centered on the middle of Germany:
#################################################################
mapGE = folium.Map(location=[latGE, lonGE], zoom_start=7)

# Get credentials from json file
#########################################################################
wksPath = Path(__file__).parents[0]
# Open json file and return content of it
def readFile(nameFile):
    path = wksPath /  nameFile
    with open(path, 'r') as file:
        content = file.read()
        return content


# Classes
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
    # r=requests.get("http://www.example.com/", headers={"content-type":"text"})
    var = requests.get(var).json()
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

# TODO: limit the data frame 'df' to a distance with 'me' and drop the rest
#Read Dataframe from CSV
df = pd.read_csv('./data/loc_cities_germany.csv', usecols={'City', 'State', 'Latitude', 'Longitude', 'Position'})

i=0
for pos in (df['Position']):

    # Generate links for different query types out of Foursquare
    datascienceGE = Link(option='search', location=pos, query='data science').venue(radius=50000,limit=80, categoryId='4d4b7105d754a06375d81259') 
    dataminingGE = Link(option='search', location=pos, query='data mining').venue(radius=50000,limit=80, categoryId='4d4b7105d754a06375d81259') 
    dataanalysisGE = Link(option='search', location=pos, query='data analysis').venue(radius=50000,limit=80, categoryId='4d4b7105d754a06375d81259') 

    try:
        # convert first to json and secondly to pandas DataFrame
        df_DSGE = get_df(datascienceGE)
        # filter the category for each row
        df_DSGE = filter_df(df_DSGE)
        df_DSGE['categories'] = df_DSGE.apply(get_category_type, axis=1)

        # instantiate a feature group for matches in the dataframe
        dataSci = folium.map.FeatureGroup()
        for latitude, longitude, companyname in zip(df_DSGE.lat, df_DSGE.lng, df_DSGE.name):
            dataSci.add_child(
                # Add markers to the map for every match
                folium.CircleMarker(
                    [latitude, longitude],
                    radius=7, # define how big you want the circle markers to be
                    color='yellow',
                    fill=True,
                    fill_color='red',
                    fill_opacity=0.6
                )
            )
            dataSci.add_child(
                # add simple popup with the name of the company when clicked
                folium.Marker(
                    location=[latitude, longitude],
                    icon=None,
                    popup=companyname,
                )
            )
        mapGE.add_child(dataSci)
        print ('{}: This city has {} results for data science'.format(df['City'].iloc[i], df_DSGE.shape[0]))
    except Exception as e:
        print ('E1000: {}, {}: This city has no results for data science'.format(e, df['City'].iloc[i]))
        pass

    try:
        df_DMGE = get_df(dataminingGE)

        df_DMGE = filter_df(df_DMGE)
        df_DMGE['categories'] = df_DMGE.apply(get_category_type, axis=1)

        dataMin = folium.map.FeatureGroup()
        for latitude, longitude, companyname in zip(df_DMGE.lat, df_DMGE.lng, df_DMGE.name):
            dataMin.add_child(
                folium.CircleMarker(
                    [latitude, longitude],
                    radius=7,
                    color='yellow',
                    fill=True,
                    fill_color='green',
                    fill_opacity=0.6
                )
            )
            dataMin.add_child(
                folium.Marker(
                    location=[latitude, longitude],
                    icon=None,
                    popup=companyname,
                )
            )
        mapGE.add_child(dataMin)
        print ('{}: This city has {} results for data mining'.format(df['City'].iloc[i], df_DMGE.shape[0]))
    except Exception as e:
        print ('E1000: {}, {}: This city has no results for data mining'.format(e, df['City'].iloc[i]))
        pass

    try:
        df_DAGE = get_df(dataanalysisGE)

        df_DAGE = filter_df(df_DAGE)
        df_DAGE['categories'] = df_DAGE.apply(get_category_type, axis=1)

        dataAna = folium.map.FeatureGroup()
        for latitude, longitude, companyname in zip(df_DAGE.lat, df_DAGE.lng, df_DAGE.name):
            dataAna.add_child(
                folium.CircleMarker(
                    [latitude, longitude],
                    radius=7,
                    color='yellow',
                    fill=True,
                    fill_color='blue',
                    fill_opacity=0.6
                )
            )
            dataAna.add_child(
                folium.Marker(
                    location=[latitude, longitude],
                    icon=None,
                    popup=companyname,
                )
            )
        mapGE.add_child(dataAna)
        print ('{}: This city has {} results for data analysis'.format(df['City'].iloc[i], df_DAGE.shape[0]))
    except Exception as e:
        print ('E1000: {}, {}: This city has no results for data analysis'.format(e, df['City'].iloc[i]))
        pass
    i+=1

# Save the map with a file
# TIP: it opens with file://<absolute path>/germany.html in your browser
mapGE.save('germany.html')


