import logging
import requests
import re
import json
import os
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

import random

from unidecode import unidecode


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
            logging.error("Timeout error", exc_info=True)
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url", exc_info=True)
        except requests.exceptions.RequestException as e:
            logging.error("Bad request", exc_info=True)
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
        try:
            if self.get_data():
                formatted_address = self.get_data(
                )['results'][0]['formatted_address']
        except KeyError:
            logging.error("Can't get formatted addresss", exc_info=True)

        return formatted_address

    def get_latitude(self):
        latitude = None
        try:
            if self.get_data():
                latitude = self.get_data(
                )['results'][0]['geometry']['location']['lat']
        except KeyError:
            logging.error("Can't get latitude", exc_info=True)

        return latitude

    def get_longitude(self):
        longitude = None
        try:
            if self.get_data():
                longitude = self.get_data(
                )['results'][0]['geometry']['location']['lng']
        except KeyError:
            logging.error("Can't get longitude", exc_info=True)

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
            "prop": "extracts|info|",
            "inprop": "url",
            "pageids": f"{pageids}",
            "explaintext": "True"}

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

    def get_page_id(self):
        page_id = None
        wiki_data = self.get_data()
        try:
            page_id = wiki_data['query']['geosearch'][0]['pageid']
        except KeyError:
            logging.error("Can't get page id", exc_info=True)

        return page_id

    def get_extract(self, page_id):
        extract = None
        wiki_data = self.get_data()
        try:
            extract = wiki_data['query']['pages'][f"{page_id}"]['extract']
        except KeyError:
            logging.error("Can't get extract", exc_info=True)

        return extract

    def get_wiki_url(self, page_id):
        fullurl = None
        wiki_data = self.get_data()
        try:
            fullurl = wiki_data['query']['pages'][f"{page_id}"]['fullurl']
        except KeyError:
            logging.error("Can't get extract", exc_info=True)

        return fullurl


class Parser:
    def __init__(self, message):
        self.message = message

    def set_lowercase(self):
        self.message = self.message.lower()
        return self.message

    def remove_accents(self):
        self.message = unidecode(self.message)
        return self.message

    def extract_questions(self):
        regex = r"""(^|(?<=[.?!,]))\s*[A-Za-z,;'\"\s\-]+\?"""
        result = []
        try:
            matches = re.finditer(regex, self.message)

            for matchNum, match in enumerate(matches):
                result.append(match.group())
            result = [element.strip() for element in result]

        except AttributeError:
            logging.error("AttributeError")

        self.message = self._pick_up_question(result)

        return self.message

    def remove_stop_words(self):

        message = self.message.split()
        try:
            with open(os.path.join('flaskr', 'static', 'fr.json'),
                      encoding='utf-8') as json_file:
                stop_words = json.load(json_file)

            result = [word for word in message if word not in stop_words]
            self.message = " ".join(result)
        except Exception:
            logging.error("Can't open fr.json", exc_info=True)

        return self.message

    def remove_apostrof(self):
        self.message = self.message.replace("'", " ")
        return self.message

    def _pick_up_question(self, dic):
        result = ""
        stemmer = SnowballStemmer("french")
        try:
            with open(os.path.join('flaskr', 'static', 'detect_word.json'),
                      encoding='utf-8') as json_file:
                words = json.load(json_file)
        except Exception:
            logging.error("Can't open detect_word.json", exc_info=True)

        stem_words = [stemmer.stem(w) for w in words]

        similarity = 0
        for sentence in dic:
            token_sentence = word_tokenize(sentence)
            stem_sentence = [stemmer.stem(s) for s in token_sentence]
            intersection = [
                value for value in stem_sentence if value in stem_words]

            if len(intersection) > similarity:
                result = sentence

        return result

    def get_section(self):
        regex = r"""(?<=(\={2}))(.*?)(?=(\={2}))"""
        result = []
        try:
            matches = re.finditer(regex, self.message, re.DOTALL)

            for matchNum, match in enumerate(matches):
                result.append(match.group())
            result = [element.strip() for element in result]

        except AttributeError:
            logging.error("AttributeError")

        self.message = self._format_section(result)

        return self.message

    def _format_section(self, result_section):
        text = ""
        i = 0
        while (i < len(result_section)-1):
            if (result_section[i] != '') and (result_section[i+1] != ''):
                if (result_section[i][0] == '='):
                    result_section[i] = result_section[i][1:]

                if (result_section[i+1][0] == '='):
                    result_section[i+1] = result_section[i+1][1:]

                text = result_section[i] + " : " + result_section[i+1]
                break
            i += 1

        return text


class Message:
    def __init__(self, data):
        self.data = data

    @classmethod
    def get_answers_from_json(cls):
        try:
            with open(os.path.join('flaskr', 'static', 'answers.json'),
                      encoding='utf-8') as json_file:
                return cls(json.load(json_file))
        except Exception:
            logging.error("Can't open answers.json", exc_info=True)

    def choose_message_for_address(self):
        message = random.choice(self.data['message_for_address'])
        return message

    def choose_message_for_story(self):
        pass


class Response:
    def __init__(self, latitude, longitude, url,
                 message_for_address, message_for_story):
        self.latitude = latitude
        self.longitude = longitude
        self.url = url
        self.message_for_address = message_for_address
        self.message_for_story = message_for_story

    def formatted_response(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "url": self.url,
            "message_for_address": self.message_for_address,
            "message_for_story": self.message_for_story
        }
