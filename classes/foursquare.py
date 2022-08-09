# -*- coding: utf-8 -*-
import requests  # library to handle requests


class Link:
    """generates a link to query the json file out of foursquare's API

    Returns:
        url: query to get desired feature
    """

    def __init__(self, option="search", version=str(20180602), **kwargs):
        self.__dict__.update(kwargs)
        self.main_URL = "https://api.foursquare.com/v2/"
        self.option = option
        self.version = str(version)

    def venue(self, query, location, client_id, client_secret, **kwargs):
        """generates this link for venues and needs of:
            option,         venues
            location,       as: latitud, longitud
            query           as: coffee, chinese food, windsurf...

        Returns:
            url: query url for venues
        """
        self.option = "/" + self.option + "?"
        self.location = "ll=" + location
        url = str(
            self.main_URL
            + "venues"
            + self.option
            + self.location
            + "&query="
            + query
            + "&client_id="
            + client_id
            + "&client_secret="
            + client_secret
            + "&v="
            + self.version
        )
        # kwargs should have the same name as in Foursquare
        for key, value in kwargs.items():
            append = "&" + key + "=" + str(value)
            url = url + append
        self.url = url
        return url

    # TODO: Finish it...
    def explore(self, client_id, client_secret):
        self.option = "/" + self.option + "?"
        self.location = "ll=" + self.location
        self.query = "&query=" + self.query
        url = str(
            self.main_URL
            + "venues"
            + self.option
            + self.location
            + self.query
            + "&client_id="
            + client_id
            + "&client_secret="
            + client_secret
            + "&v="
            + self.version
        )
        return url

    def getResponse(self):
        self.response = requests.get(self.url)
        return self.response

    def hasError(self):
        result = False
        self.js = self.response.json()
        if self.js["meta"]["code"] == 402:
            result = True
            self.getError()
        return result

    def getError(self):
        return self.js["meta"]["code"]
