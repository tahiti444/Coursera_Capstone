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


# Search example
coffeeNY = Link(option='search', location='40.7,-74', query='coffee').venue()
print(coffeeNY)

# explore example
exploreNY = Link(option='explore', location='40.7,-74', query='coffee').explore()
print(exploreNY)

# FIXME: trending example
# trendingNY = Link(option='trending', location='40.7,-74', query='coffee').venue()
# print(trendingNY)


# Section_Sample
###############################################################