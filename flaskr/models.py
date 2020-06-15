import logging
import requests

import configuration.config as config

config.load('./configuration/config.yml')


class GoogleApi:
    def __init__(self):
        self.url = config.value['GOOGLE']['URL']
        self.api_key = config.value['GOOGLE']['API_KEY']
        self._data = []

    def send_request(self, place):
        payload = {'address': place, 'key': self.api_key}
        try:
            response = requests.get(self.url, params=payload)
        except requests.exceptions.Timeout:
            logging.error("Timeout error")
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url")
        except requests.exceptions.RequestException as e:
            logging.error("Bad request")
            raise SystemExit(e)

        if response.status_code == 200:
            self._data = response.json()
            return response.json()
        else:
            return None

    def get_data(self):
        return self._data

    def get_formatted_address(self):
        formatted_address = []

        if self.get_data():
            formatted_address = self.get_data(
            )['results'][0]['formatted_address']

        return formatted_address

    def get_latitude(self):
        latitude = None

        if self.get_data():
            latitude = self.get_data(
            )['results'][0]['geometry']['location']['lat']

        return latitude

    def get_longitude(self):
        longitude = None

        if self.get_data():
            longitude = self.get_data(
            )['results'][0]['geometry']['location']['lng']

        return longitude


class WikiApi:
    def __init__(self):
        self.url = config.value['MEDIA_WIKI']['URL']
        self._data = []

    def send_geosearch_request(self, latitude, longitude):
        payload = {
                    "action": "query",
                    "format": "json",
                    "list": "geosearch",
                    "gscoord": f"{latitude}|{longitude}",
                    "gsradius": "1000",
                    "gslimit": "1"}

        try:
            response = requests.get(self.url, params=payload)
        except requests.exceptions.Timeout:
            logging.error("Timeout error")
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url")
        except requests.exceptions.RequestException as e:
            logging.error("Bad request")
            raise SystemExit(e)

        if response.status_code == 200:
            self._data = response.json()
            return response.json()
        else:
            return None

    def send_pageids_request(self, pageids):
        payload = {
                    "action": "query",
                    "format": "json",
                    "prop": "extracts",
                    "pageids": f"{pageids}"}

        try:
            response = requests.get(self.url, params=payload)
        except requests.exceptions.Timeout:
            logging.error("Timeout error")
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url")
        except requests.exceptions.RequestException as e:
            logging.error("Bad request")
            raise SystemExit(e)

        if response.status_code == 200:
            self._data = response.json()
            return response.json()
        else:
            return None


class Parser:
    def __init__(self):
        pass


class Message:
    def __init__(self):
        pass


class Response:
    def __init__(self, formatted_address, latitude, longitude,
                 message_for_address, message_for_story):
        self.formatted_address = formatted_address
        self.latitude = latitude
        self.longitude = longitude
        self.message_for_address = message_for_address
        self.message_for_story = message_for_story

    def formatted_response(self):
        return {
            "formatted_address": self.formatted_address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "message_for_address": self.message_for_address,
            "message_for_story": self.message_for_story
        }
