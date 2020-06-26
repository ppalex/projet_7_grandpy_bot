import json
import os

from flaskr.models import GoogleApi, Message, Parser, Response, WikiApi
from flaskr.run import app


class TestGoogleApi:
    """This class contains all the methods to test the Google API."""

    class MockRequestGet:
        """This class mock the get method from Request for google api."""

        def __init__(self, url, params=None):
            """Constructor of the class MockRequestGet.

            Args:
                url (String): Url endpoint for the api.
            """
            self.status_code = 200

        def json(self):
            """This method returns the data get from the request into JSON.

            Returns:
                [JSON]: Contains the data from the api.
            """
            return {"results": [
                    {"address_components": [{"long_name": "Paris"}],
                        "formatted_address":
                            "7 Cité Paradis, 75010 Paris, France",
                        "geometry": {"location":
                                     {"lat": 48.874847, "lng": 2.350487}}}
                    ],
                    "status": "OK"}

    def test_send_request(self, monkeypatch):
        """This method tests the send request method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """

        results = {
            "results": [
                {
                    "address_components": [
                        {"long_name": "Paris"}],
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {"location":
                                 {"lat": 48.874847, "lng": 2.350487}}
                }
            ],
            "status": 'OK'
        }

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        response = GoogleApi().send_request("OpenClassrooms")

        assert response == results

    def test_get_formatted_address(self, monkeypatch):
        """This method tests the send request method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = "7 Cité Paradis, 75010 Paris, France"

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")
        formatted_address = google_api.get_formatted_address()

        assert formatted_address == result

    def test_get_latitude(self, monkeypatch):
        """This method tests the get_latitude method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = 2.350487

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        longitude = google_api.get_longitude()

        assert longitude == result

    def test_get_longitude(self, monkeypatch):
        """This method tests the get longitude method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = 48.874847

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        latitude = google_api.get_latitude()

        assert latitude == result

    def test_get_status(self, monkeypatch):
        """This method tests the get_status method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = "OK"

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        status = google_api.get_status()

        assert status == result

    def test_set_status(self, monkeypatch):
        """This method tests set_status method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = "NOT OK"

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        google_api.set_status("NOT OK")
        status = google_api.get_status()

        assert status == result


class TestWikiApi:
    """This class contains all the methods to test the Wiki API."""
    class MockRequestGetGeosearch:
        """This class mock the get method from Request for wikimedia."""

        def __init__(self, url, params=None):
            """Constructor of the class MockRequestGetGeosearch.

            Args:
                url (String): Url endpoint for the api.
            """
            self.status_code = 200

        def json(self):
            return {'batchcomplete': '',
                    'query': {'geosearch': [{'pageid': 51281575,
                                             'ns': 0,
                                             'title': 'Studio Berçot',
                                             'lat': 48.8738,
                                             'lon': 2.3515,
                                             'dist': 138,
                                             'primary': ''}]}}

    class MockRequestGetPageId:
        def __init__(self, url, params=None):
            """Constructor of the class MockRequestGet.

            Args:
                url (String): Url endpoint for the api.
            """
            self.status_code = 200

        def json(self):
            """This method returns the data get from the request into JSON.

            Returns:
                [JSON]: Contains the data from the api.
            """
            return {"batchcomplete": "",
                    "warnings": {
                        "extracts": {}},
                    "query": {
                        "pages": {
                            "18618509": {
                                "pageid": 18618509,
                                "ns": 0,
                                "title": "Wikimedia Foundation",
                                "extract": "Text description of the page",
                                "fullurl": "https://fr.wikipedia.org/wiki/"}}}}

    def test_send_geosearch_request(self, monkeypatch):
        """This method tests send_geosearch_request method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """

        results = {'batchcomplete': '',
                   'query': {'geosearch': [{'pageid': 51281575,
                                            'ns': 0,
                                            'title': 'Studio Berçot',
                                            'lat': 48.8738,
                                            'lon': 2.3515,
                                            'dist': 138,
                                            'primary': ''}]}}

        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetGeosearch)
        wikimedia_api = WikiApi()
        response = wikimedia_api.send_geosearch_request(48.8738, 2.3515)

        assert response == results

    def test_send_pageids_request(self, monkeypatch):
        """This method tests send_pageids_request method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """

        results = {"batchcomplete": "",
                   "warnings": {
                       "extracts": {}},
                   "query": {
                       "pages": {
                           "18618509": {
                               "pageid": 18618509,
                               "ns": 0,
                               "title": "Wikimedia Foundation",
                               "extract": "Text description of the page",
                               "fullurl": "https://fr.wikipedia.org/wiki/"}}}}

        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetPageId)
        wikimedia_api = WikiApi()
        response = wikimedia_api.send_pageids_request(18618509)

        assert response == results

    def test_get_extract(self, monkeypatch):
        """This method tests get_extract method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """

        result = "Text description of the page"
        page_id = 18618509

        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetPageId)
        wikimedia_api = WikiApi()
        wikimedia_api.send_pageids_request(page_id)

        extract = wikimedia_api.get_extract(page_id)

        assert extract == result

    def test_get_page_id(self, monkeypatch):
        """This method tests get_page_id method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = 51281575

        monkeypatch.setattr('flaskr.models.requests.get',
                            self.MockRequestGetGeosearch)
        wikimedia_api = WikiApi()
        wikimedia_api.send_geosearch_request(48.8738, 2.3515)

        page_id = wikimedia_api.get_page_id()

        assert page_id == result

    def test_get_wiki_url(self, monkeypatch):
        """This method tests get_wiki_url method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        result = "https://fr.wikipedia.org/wiki/"
        page_id = 18618509

        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetPageId)
        wikimedia_api = WikiApi()
        wikimedia_api.send_pageids_request(page_id)

        fullurl = wikimedia_api.get_wiki_url(page_id)

        assert fullurl == result


class TestParser:
    """This class contains all the methods to test the Parser."""

    def test_set_lowercase(self):
        """This method tests set_lowercase method."""
        result = "hello world"
        message = "HELLO WORLD"
        parser = Parser(message)

        assert parser.set_lowercase() == result

    def test_remove_accents(self):
        """This method tests remove_accents method."""
        result = "eeaaaun"
        message = "éèàâäùñ"
        parser = Parser(message)

        assert parser.remove_accents() == result

    def test_extract_questions(self):
        """This method test extract_questions method."""
        result = """Est-ce que tu pourrais m indiquer
                    l adresse de la tour eiffel?"""

        message = """"Bonsoir Grandpy, Comment vas-tu?
                    J espere que tu as passé une belle semaine.
                    Est-ce que tu pourrais m indiquer
                    l adresse de la tour eiffel?"""

        parser = Parser(message)

        assert parser.extract_questions() == result

    def test_remove_stop_words(self):
        """This method tests remove_stop_words method."""
        result = ""

        with open(os.path.join('flaskr', 'static', 'fr.json'),
                  encoding='utf-8') as json_file:
            message = json.load(json_file)

        message = " ".join(message)
        parser = Parser(message)

        assert parser.remove_stop_words() == result

    def test_remove_apostrof(self):
        """This method tests remove_apostrof method."""
        result = "l m n o p "
        message = "l'm'n'o'p'"
        parser = Parser(message)

        assert parser.remove_apostrof() == result

    def test_pick_up_question(self):
        """This method test pick_up_question method."""
        message = ["donne moi l'adresse de",
                   "je me trouve et je veux acceder depuis ma position"]
        result = "je me trouve et je veux acceder depuis ma position"

        parser = Parser("")

        assert parser._pick_up_question(message) == result

    def test_get_section(self):
        """This method test get_section method."""
        result = "1ère section : contenu de la section"
        message = """ Premier paragraphe == 1ère section == contenu de la section
                        == 2ème section == contenu de la section"""

        parser = Parser(message)

        assert parser.get_section() == result


class TestResponse:
    """This class contains all the methods to test Response."""

    def test_formatted_response(self):
        """This method tests fromatted_response method."""
        result = {
            "status": "OK",
            "latitude": 2.350487,
            "longitude": 48.874847,
            "url": "https://fr.wikipedia.org/wiki/",
            "message_for_address": "7 Cité Paradis, 75010 Paris, France",
            "message_for_story": "story text",
            "message_for_error": "error text"
        }

        response = Response("OK",
                            2.350487,
                            48.874847,
                            "https://fr.wikipedia.org/wiki/",
                            "7 Cité Paradis, 75010 Paris, France",
                            "story text",
                            "error text")

        assert response.formatted_response() == result


class TestMessage:
    """This class contains all the methods to test the Message."""

    def test_get_message_for_address(self, monkeypatch):
        """This method tests message_for_address method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        def mock_json_load(file):
            """This method mock the json_load method.
            Returns:
                [JSON]: Contains the message for address.
            """
            return {"message_for_address":
                    ["Bien sûr mon poussin ! La voici:"]}

        result = "Bien sûr mon poussin ! La voici:"
        monkeypatch.setattr('flaskr.models.json.load',
                            mock_json_load)
        data_message = Message.get_answers_from_json()

        assert data_message.get_message_for_address() == result

    def test_get_message_for_story(self, monkeypatch):
        """This method tests message_for_story method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        def mock_json_load(file):
            """This method mock the json_load method.
            Returns:
                [JSON]: Contains the message for story.
            """
            return {"message_for_story":
                    ["story"]}

        result = "story"
        monkeypatch.setattr('flaskr.models.json.load',
                            mock_json_load)
        data_message = Message.get_answers_from_json()

        assert data_message.get_message_for_story() == result

    def test_get_message_for_error(self, monkeypatch):
        """This method tests message_for_error method.

        Args:
            monkeypatch (MonkeyPatch): Method from pytest to replace a method
            by another and go back to the initial method after the process
            instructions are done.
        """
        def mock_json_load(file):
            """This method mock the json_load method.
            Returns:
                [JSON]: Contains the message for story.
            """
            return {"message_for_error":
                    ["error"]}

        result = "error"
        monkeypatch.setattr('flaskr.models.json.load',
                            mock_json_load)
        data_message = Message.get_answers_from_json()

        assert data_message.get_message_for_error() == result


class TestAppRoutes:
    """This class contains all the methods to test the routes from the flask
    app."""

    def test_index(self):
        """This method tests the get method for index route."""
        client = app.test_client()
        url = '/'

        response = client.get(url)

        assert response.status_code == 200

    def test_form(self):
        """This method tests the post method on form routes."""
        client = app.test_client()
        url = '/form'

        mock_request_data = {
            "user_text": "Texte de l'utilisateur"
        }

        response = client.post(url, data=mock_request_data)
        assert response.status_code == 200
