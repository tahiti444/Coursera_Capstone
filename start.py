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


# TODO:missing url_from_users and url_from_tips...
# Classes
##########################################################################
'''
class Link() -> generates a link to query the json file out of foursquare's API:
    method url_from_venue -> generates this link for venues and needs of: 
        option,         venues
        location,       as: latitud, longitud
        query           as: coffee, chinese food, windsurf...
'''
class Link(object):

    global main_URL, client_id, client_secret, version

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def url_from_venue(self):
        self.option = str(self.option) + '/search?'
        self.location = 'll=' + self.location
        self.query = '&query=' + self.query
        return (str(main_URL+self.option+self.location+self.query+'&client_id='+client_id+'&client_secret='+client_secret+'&v='+version))



coffeeNY = Link(option='venues', location='40.7,-74', query='coffee').url_from_venue()
print(coffeeNY)






# Section_Sample
###############################################################