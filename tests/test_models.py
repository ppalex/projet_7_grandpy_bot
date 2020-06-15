from flaskr.models import GoogleApi, WikiApi, Response


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

    class MockRequestGet:
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

    def test_send_geosearch_request(self, monkeypatch):
        results = {'batchcomplete': '',
                   'query': {'geosearch': [{'pageid': 51281575,
                                            'ns': 0,
                                            'title': 'Studio Berçot',
                                            'lat': 48.8738,
                                            'lon': 2.3515,
                                            'dist': 138,
                                            'primary': ''}]}}

        monkeypatch.setattr("flaskr.models.requests.get", self.MockRequestGet)
        wikimedia_api = WikiApi()
        response = wikimedia_api.send_geosearch_request(48.8738, 2.3515)

        assert response == results


class TestParser:
    pass


class TestResponse:

    def test_formatted_response(self):

        result = {
            "formatted_address": "7 Cité Paradis, 75010 Paris, France",
            "latitude": 2.350487,
            "longitude": 48.874847,
            "message_for_address": "",
            "message_for_story": ""
        }

        response = Response(
            "7 Cité Paradis, 75010 Paris, France", 2.350487,  48.874847, "", "")

        assert response.formatted_response() == result
