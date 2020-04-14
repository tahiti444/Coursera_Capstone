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
import json

wksPath = Path(__file__).parents[0]

def readFile(nameFile):
    path = wksPath /  nameFile
    with open(path, 'r') as file:
        content = file.read()
        return content

# creating an object of URL for foursquare's API
main_URL = 'https://api.foursquare.com/v2/'

# TODO:generalize this for future...
# What do you want to search?
about = 'venues/search?' # venues, users or tips
location = '40.7,-74'
what = 'coffee'
query = 'll='+str(location)+'&query='+what

# inizializate id credentials
id_key = readFile('credentials.json')
id_key = json.loads(id_key)
client_id = id_key["client_id"]
client_secret = id_key["client_secret"]

version = str(20180602)
credentials = '&client_id='+client_id+'&client_secret='+client_secret+'&v='+version

# forming complete url
foursquare_URL = main_URL + about + query + credentials 

print (foursquare_URL)





# Section_Sample
###############################################################