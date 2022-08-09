# -*- coding: utf-8 -*-

# from msilib.schema import Class
from geopy.geocoders import (
    Nominatim,
)  # module to convert an address into latitude and longitude values
import folium  # plotting library


class CenteredChart:
    """returns a centered chart readable with HTML
    
    Attributes:
        country_name
        location
        lat
        lon       
    
    Methods:
        getCoordinates (string): Returns a string with coordinates, eg. (12,34)
        getCenteredChart (folium.Map): Returns a centered map with a zoom that equals 7
    """

    def __init__(self, **kwargs):
        """initialization
        kwargs:
            - country = Germany (default)
        """
        self.__dict__.update(kwargs)
        if "country" in kwargs:
            self.setCountry(kwargs["country"])
        else:
            self.setCountry(country="Germany")
        self.setLocation()
        self.setCoordinates()
        self.setCenteredChart()

    def setCountry(self, country):
        """set country name
        Args:
            country (string): country name
        """
        self.country = country

    def setLocation(self):
        geolocator = Nominatim(user_agent="aiFinder")
        self.location = geolocator.geocode(self.country)

    def setCoordinates(self):
        self.lat = self.location.latitude  # --> Center
        self.lon = self.location.longitude  # --> Center

    def getCoordinates(self):
        # Returns a string with coordinates, eg. (12,34)
        return str(str(self.lat) + "," + str(self.lon))

    def setCenteredChart(self):
        self.map = folium.Map(location=[self.lat, self.lon], zoom_start=7)

    def getCenteredChart(self):
        # Returns a centered map with a zoom that equals 7
        return folium.Map(location=[self.lat, self.lon], zoom_start=7)

    def setFeatureGroup(self):
        self.featureGroup = folium.map.FeatureGroup()

    def drawPoint(self, latitude, longitude, name):
        self.featureGroup.add_child(
            folium.CircleMarker(
                [latitude, longitude],
                radius=7,  # define how big you want the circle markers to be
                color="yellow",
                fill=True,
                fill_color="red",
                fill_opacity=0.6,
            )
        )
        self.featureGroup.add_child(
            # add simple popup with the name of the company when clicked
            folium.Marker(location=[latitude, longitude], icon=None, popup=name,)
        )
        self.map.add_child(self.featureGroup)

    def saveMap(self, path="./data/popupmap.html"):
        self.map.save(path)


"""
Uncomment if want to actualize cities
"""

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

"""
Commented out after saving dataframe!
"""
