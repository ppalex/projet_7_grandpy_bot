from flaskr.models import GoogleApi, WikiApi, Response, Parser, Message

import json
import os

from nltk.stem import SnowballStemmer


class TestGoogleApi:

    class MockRequestGet:
        def __init__(self, url, params=None):
            self.status_code = 200

        def json(self):
            return {"results": [
                    {"address_components": [{"long_name": "Paris"}],
                        "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                        "geometry": {"location":
                                     {"lat": 48.874847, "lng": 2.350487}}}
                    ]}

    def test_send_request(self, monkeypatch):
        results = {
            "results": [
                {
                    "address_components": [
                        {"long_name": "Paris"}],
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {"location":
                                 {"lat": 48.874847, "lng": 2.350487}}
                }
            ]
        }

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        response = GoogleApi().send_request("OpenClassrooms")

        assert response == results

    def test_get_formatted_address(self, monkeypatch):
        result = "7 Cité Paradis, 75010 Paris, France"

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")
        formatted_address = google_api.get_formatted_address()

        assert formatted_address == result

    def test_get_latitude(self, monkeypatch):
        result = 2.350487

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        longitude = google_api.get_longitude()

        assert longitude == result

    def test_get_longitude(self, monkeypatch):
        result = 48.874847

        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        google_api.send_request("OpenClassrooms")

        latitude = google_api.get_latitude()

        assert latitude == result


class TestWikiApi:

    class MockRequestGetGeosearch:
        def __init__(self, url, params=None):
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
            self.status_code = 200

        def json(self):
            return {"batchcomplete": "",
                    "warnings": {
                        "extracts": {}},
                    "query": {
                        "pages": {
                            "18618509": {
                                "pageid": 18618509,
                                "ns": 0,
                                "title": "Wikimedia Foundation",
                                "extract": "Text description of the page"}}}}

    def test_send_geosearch_request(self, monkeypatch):

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

        results = {"batchcomplete": "",
                   "warnings": {
                       "extracts": {}},
                   "query": {
                       "pages": {
                           "18618509": {
                               "pageid": 18618509,
                               "ns": 0,
                               "title": "Wikimedia Foundation",
                               "extract": "Text description of the page"}}}}

        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetPageId)
        wikimedia_api = WikiApi()
        response = wikimedia_api.send_pageids_request(18618509)

        assert response == results

    def test_get_extract(self, monkeypatch):
        
        result = "Text description of the page"
        page_id = 18618509
        
        monkeypatch.setattr("flaskr.models.requests.get",
                            self.MockRequestGetPageId)
        wikimedia_api = WikiApi()
        response = wikimedia_api.send_pageids_request(page_id)
              
        extract = wikimedia_api.get_extract(page_id)
        
        assert extract == result

    def test_get_page_id(self, monkeypatch):
        result = 51281575

        monkeypatch.setattr('flaskr.models.requests.get',
                            self.MockRequestGetGeosearch)
        wikimedia_api = WikiApi()
        wikimedia_api.send_geosearch_request(48.8738, 2.3515)

        page_id = wikimedia_api.get_page_id()

        assert page_id == result


class TestParser:
    def test_set_lowercase(self):
        result = "hello world"
        message = "HELLO WORLD"
        parser = Parser(message)
        
        assert parser.set_lowercase() == result       

    def test_remove_accents(self):
        result = "eeaaaun"
        message = "éèàâäùñ"
        parser = Parser(message)
        
        assert parser.remove_accents() == result
        
    def test_extract_questions(self):
        result = "Est-ce que tu pourrais m indiquer l adresse de la tour eiffel?"
        
        message = """"Bonsoir Grandpy, Comment vas-tu?
                        J espere que tu as passé une belle semaine.
                        Est-ce que tu pourrais m indiquer l adresse de la tour eiffel?""" 
                        
        parser = Parser(message)
        
        assert parser.extract_questions() == result       
        
        
    def test_remove_stop_words(self):
        result = ""
        
        with open(os.path.join('flaskr', 'static', 'fr.json'), encoding='utf-8') as json_file:
            message = json.load(json_file)
            
        message = " ".join(message)        
        parser = Parser(message)        
        
        assert parser.remove_stop_words() == result
        
    def test_remove_apostrof(self):
        result = "l m n o p "
        message = "l'm'n'o'p'"
        parser = Parser(message)
        
        assert parser.remove_apostrof() == result
        
    def test_pick_up_question(self):
        message = ["donne moi l'adresse de", "je me trouve et je veux acceder depuis ma position"]
        result = "je me trouve et je veux acceder depuis ma position"
        
        parser = Parser("")
        
        assert parser._pick_up_question(message) == result
        
    
    def test_gest_section(self):
        result = "1ère section contenu de la section" 
        message = """ Premier paragraphe == 1ère section == contenu de la section 
                        == 2ème section == contenu de la section"""
                        
        parser = Parser(message)
        
        assert parser.get_section() == result
    

class TestResponse:

    def test_formatted_response(self):

        result = {
            "latitude": 2.350487,
            "longitude": 48.874847,
            "message_for_address": "7 Cité Paradis, 75010 Paris, France",
            "message_for_story": "story text"
        }

        response = Response(2.350487,
                            48.874847, 
                            "7 Cité Paradis, 75010 Paris, France",
                            "story text")

        assert response.formatted_response() == result
        
class TestMessage:
    
    def test_choose_message_for_address(self, monkeypatch):
        
        def mock_json_load(file):
            return {"message_for_address": 
                    ["Bien sûr mon poussin ! La voici:"]}
        
        result = "Bien sûr mon poussin ! La voici:"        
        monkeypatch.setattr('flaskr.models.json.load',
                            mock_json_load)        
        data_message = Message.get_answers_from_json()
        
        assert data_message.choose_message_for_address() == result
    
    def test_choose_message_for_story(self, monkeypatch):
        def mock_json_load(file):
            return {"message_for_story": 
                    [""]}
        
        result = ""        
        monkeypatch.setattr('flaskr.models.json.load',
                            mock_json_load)        
        data_message = Message.get_answers_from_json()
        
        assert data_message.choose_message_for_address() == result
