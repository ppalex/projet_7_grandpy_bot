from flaskr.models import GoogleApi

class TestGoogleApi:
    
    class MockRequestGet:
        def __init__(self, url, params=None):
            self.status_code = 200
            
        def json(self):
            return {
                "results" : [
                    {
                        "address_components" : [
                                                {"long_name" : "Paris"}],
                        "formatted_address" : "7 Cité Paradis, 75010 Paris, France",
                        "geometry": {"location": {"lat": 48.874847, "lng": 2.350487}}
                        }                       
                    ]                                   
                }     
    
        
    def test_send_request(self, monkeypatch):
        results =  {
                "results" : [
                    {
                        "address_components" : [
                                                {"long_name" : "Paris"}],
                        "formatted_address" : "7 Cité Paradis, 75010 Paris, France",
                        "geometry": {"location": {"lat": 48.874847, "lng": 2.350487}}
                        }                 
                    ]                                  
                }        
        
        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
               
        assert GoogleApi().send_request("OpenClassrooms") == results
    
    
    def test_get_formatted_address(self, monkeypatch):
        result =  "7 Cité Paradis, 75010 Paris, France"
        
        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        response = google_api.send_request("OpenClassrooms")
        formatted_address = google_api.get_formatted_address()
        
        assert formatted_address == result
        
        
    def test_get_latitude(self, monkeypatch):
        result = 2.350487
        
        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        response = google_api.send_request("OpenClassrooms")
        
        longitude = google_api.get_longitude()
        
        assert longitude == result
    
    def test_get_longitude(self, monkeypatch):
        result = 48.874847
        
        monkeypatch.setattr('flaskr.models.requests.get', self.MockRequestGet)
        google_api = GoogleApi()
        response = google_api.send_request("OpenClassrooms")
        
        latitude = google_api.get_latitude()
        
        assert latitude == result
    
    
class TestWikiApi:
    pass
    
    
class TestParser:
    pass