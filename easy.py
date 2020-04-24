'''
Log:
    - 22.04.2020: Program from start.py exported: it is much easier this coding!
'''


# Import libraries
###############################################################
from pathlib import Path

# working with json and tranforming json file into a pandas dataframe library
import json
from pandas.io.json import json_normalize
import requests # library to handle requests

# Data-Science tools
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

# Maps generation
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import folium # plotting library

# libraries for displaying images
# from IPython.display import Image 
# from IPython.core.display import HTML 

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


# Global initialization
#########################################################################
# read json file and save it
id_key = readFile('credentials.json')
id_key = json.loads(id_key)
# inizializate id credentials
my_client_id = id_key["client_id"]
my_client_secret = id_key["client_secret"]


# Functions:
#################################################################
# function to avoid generating test variables:
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


# TODO: generate a dictionary for the Foursquare API:
#################################################################
'''
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
def explore_url(location, query, r, limit, version):
    url = 'https://api.foursquare.com/v2/venues/explore'
    # for key, value in kwargs.items():
    #     if ((key=='version') & (value==None)):
    #         version=str(20180602)    
    #     else:
    #         version=version
    params = dict(
        client_id=my_client_id,
        client_secret=my_client_secret,
        v=version,
        ll=location,
        query=query,
        radius=r,
        limit=limit
    )
    # resp = requests.get(url=url, params=params)
    jdata = requests.get(url=url, params=params).json()
    jstr = json.dumps(jdata, sort_keys=True, indent=2)
    # ans = json.loads(jstr)
    ans = dict (
        json_data=jdata,
        json_string=jstr        
    )
    return ans


coffeeNY = explore_url(str('40.7243,-74.0018'), 'coffee', 500, 30, str(20180602))
coffeeNY = coffeeNY['json_data']['response']['groups'][0]['items']
coffeeNYstr = json.dumps(coffeeNY, sort_keys=True, indent=2)
with open('./test.json','w') as file:
    file.write(coffeeNYstr)


df_unclean = json_normalize(coffeeNY)
df_unclean.to_csv('./test.csv')
print (df_unclean.columns)
'''
Index(['referralId', 'reasons.count', 'reasons.items', 'venue.id',
       'venue.name', 'venue.location.address', 'venue.location.lat',
       'venue.location.lng', 'venue.location.labeledLatLngs',
       'venue.location.distance', 'venue.location.postalCode',
       'venue.location.cc', 'venue.location.city', 'venue.location.state',
       'venue.location.country', 'venue.location.formattedAddress',
       'venue.categories', 'venue.photos.count', 'venue.photos.groups',
       'venue.location.crossStreet', 'venue.venuePage.id', 'venue.delivery.id',
       'venue.delivery.url', 'venue.delivery.provider.name',
       'venue.delivery.provider.icon.prefix',
       'venue.delivery.provider.icon.sizes',
       'venue.delivery.provider.icon.name', 'venue.location.neighborhood'],
      dtype='object')
'''
print (df_unclean.head(10))


# TODO: retrieve data from json! it works but had no time to check wch keys are needed
# print (coffee['response']['venues']) # not working
