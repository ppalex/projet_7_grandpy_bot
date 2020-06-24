import json
import logging
import os
import random
import re

import requests
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from unidecode import unidecode

import configuration.config as config

config.load('./configuration/config.yml')


class GoogleApi:
    def __init__(self):
        """Constructor of the class GoogleApi
        """
        self.url = config.value['GOOGLE']['URL']
        self.api_key = config.value['GOOGLE']['API_KEY']
        self._data = []

    def send_request(self, place):
        """This method send a request on the google api end point.

        Args:
            place (String): place to be sent to the api.

        Raises:
            SystemExit: If exception is raised.

        Returns:
            [JSON]: Response from the request. Contains the data.
        """
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
        """This method get the data gathered from the api request.

        Returns:
            [JSON]: Response from the request. Contains the data.
        """
        return self._data

    def get_formatted_address(self):
        """This method get the address of the place.

        Returns:
            [String]: Address.
        """
        formatted_address = ""
        try:
            if self.get_data():
                formatted_address = self.get_data(
                )['results'][0]['formatted_address']
        except KeyError:
            logging.error("Can't get formatted addresss", exc_info=True)

        return formatted_address

    def get_latitude(self):
        """This method get the latitude of a place.

        Returns:
            [Int]: Represents the latitude.
        """
        latitude = None
        try:
            if self.get_data():
                latitude = self.get_data(
                )['results'][0]['geometry']['location']['lat']
        except KeyError:
            logging.error("Can't get latitude", exc_info=True)

        return latitude

    def get_longitude(self):
        """This method get the longitude of a place.

        Returns:
            [Int]: Represents the longitude.
        """
        longitude = None
        try:
            if self.get_data():
                longitude = self.get_data(
                )['results'][0]['geometry']['location']['lng']
        except KeyError:
            logging.error("Can't get longitude", exc_info=True)

        return longitude

    def get_status(self):
        """This method get the status of the data.

        Returns:
            [String]: Status is: OK or NOT OK
        """
        status = ""

        try:
            if self.get_data():
                status = self.get_data(
                )['status']
        except KeyError:
            logging.error("Can't get status", exc_info=True)

        return status

    def set_status(self, new_status):
        """This method modifies the status of the data.
        """
        try:
            if self.get_data():
                self.get_data()['status'] = new_status
        except KeyError:
            logging.error("Can't get status", exc_info=True)


class WikiApi:
    def __init__(self):
        """Constructor of the class WikiApi
        """
        self.url = config.value['MEDIA_WIKI']['URL']
        self._data = []

    def send_geosearch_request(self, latitude, longitude):
        """This method send a request on the wiki api end point.
        The request is based on coordinates.

        Args:
            latitude (Int): Latitude of the place.
            longitude (Int): Longitude of the place.

        Raises:
            SystemExit: If exception is raised.

        Returns:
            [JSON]: Response from the request. Contains the data.
        """
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
        """This method send a request on the wiki api end point.
        The request is based on the page_id of the wiki page.

        Args:
            pageids (Int): id.

        Raises:
            SystemExit: If exception is raised.

        Returns:
            [JSON]: Response from the request. Contains the data.
        """

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
        """This method get the data gathered from the api request.

        Returns:
            [JSON]: Response from the request. Contains the data.
        """
        return self._data

    def get_page_id(self):
        """This method get the page id from the data.

        Returns:
            [Int]: Page id.
        """
        wiki_data = self.get_data()
        try:
            page_id = wiki_data['query']['geosearch'][0]['pageid']
        except Exception:
            logging.error("Can't get page id", exc_info=True)
            page_id = None

        return page_id

    def get_extract(self, page_id):
        """This method get the extraction text from wikipedia.

        Args:
            page_id (Int): Page id.

        Returns:
            [String]: Contains the text extracted.
        """
        wiki_data = self.get_data()
        try:
            extract = wiki_data['query']['pages'][f"{page_id}"]['extract']
        except KeyError:
            logging.error("Can't get extract", exc_info=True)
            extract = None

        return extract

    def get_wiki_url(self, page_id):
        """This method get the url from the wikipedia page.

        Args:
            page_id (Int): Page id.

        Returns:
            [String]: url.
        """
        fullurl = None
        wiki_data = self.get_data()
        try:
            fullurl = wiki_data['query']['pages'][f"{page_id}"]['fullurl']
        except KeyError:
            logging.error("Can't get extract", exc_info=True)

        return fullurl


class Parser:
    def __init__(self, message):
        """Constructor of the class Parser
        """
        self.message = message

    def set_lowercase(self):
        """This method put the uppercase letter to lowercase into
        a string.

        Returns:
            [String]: Contains only lowercase letter.
        """
        self.message = self.message.lower()
        return self.message

    def remove_accents(self):
        """This method remove letter with accentuation and replace it with
        the letter without accent.

        Returns:
            [String]: Contains letters without accents.
        """
        self.message = unidecode(self.message)
        return self.message

    def extract_questions(self):
        """This method extracts questions from a string and return one
        question.

        Returns:
            [String]: Contains a question.
        """
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
        """This method removes stop words from a string.
        The list of stopwords is located in 'static\fr.json'

        Returns:
            [String]: Contains a string without stopwords.
        """

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
        """This method removes apostrofes from a string.

        Returns:
            [String]: Contains a string without apostrofes.
        """
        self.message = self.message.replace("'", " ")
        return self.message

    def _pick_up_question(self, question_list):
        """This method choose an appropriate question for the wiki_api from
        a list a question.

        Args:
            question_list (List): Contains a list of question.

        Returns:
            [String]: One question.
        """
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
        for sentence in question_list:
            token_sentence = word_tokenize(sentence)
            stem_sentence = [stemmer.stem(s) for s in token_sentence]
            intersection = [
                value for value in stem_sentence if value in stem_words]

            if len(intersection) > similarity:
                result = sentence

        return result

    def get_section(self):
        """This method get a section from the entire wikipedia page.

        Returns:
            [String]: One section the wikipedia page.
        """
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
        """This method removes section separator from the wikipedia page.
         Format: Section title: Content.

        Args:
            result_section (String): Contains the wikipedia page with a section
            separated with "=".

        Returns:
            [String]: Contains the text without section separator.
        """
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
        """Constructor of the class Message.
        """
        self.data = data

    @classmethod
    def get_answers_from_json(cls):
        """This class method create a message from the data contained
        in the 'answer.json' file.

        Returns:
            [Message]: Object which contains a bunch of answers.
        """
        try:
            with open(os.path.join('flaskr', 'static', 'answers.json'),
                      encoding='utf-8') as json_file:
                return cls(json.load(json_file))
        except Exception:
            logging.error("Can't open answers.json", exc_info=True)

    def get_message_for_address(self):
        """This method get a message that will be send to give the address.

        Returns:
            [String]: Message for address.
        """
        message = random.choice(self.data['message_for_address'])
        return message

    def get_message_for_story(self):
        pass

    def get_message_for_error(self):
        """This method get a message that will be send to give the story.

        Returns:
            [String]: Message for story.
        """
        message = random.choice(self.data['message_for_error'])
        return message


class Response:
    def __init__(self, status, latitude, longitude, url,
                 message_for_address, message_for_story,
                 message_for_error):
        """Constructor of the class Response.
        """
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.url = url
        self.message_for_address = message_for_address
        self.message_for_story = message_for_story
        self.message_for_error = message_for_error

    def formatted_response(self):
        """This method return the formatted response and all the data
        that will be displayed for the user of the app.

        Returns:
            [Dict]: Contains status, latitude, longitude, url, and messages.
        """
        return {
            "status": self.status,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "url": self.url,
            "message_for_address": self.message_for_address,
            "message_for_story": self.message_for_story,
            "message_for_error": self.message_for_error
        }
