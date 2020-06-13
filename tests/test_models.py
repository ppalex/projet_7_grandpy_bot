from flaskr.models import GoogleApi

class TestGoogleApi: 
    
        
    def test_send_request(self, monkeypatch):
        place = "Paris"
        results = {
                    "results" : [
                        {
                            "address_components" : [
                                                    {
                                                    "long_name" : place
                                                    }]}]}
        
        class MockRequestGet:
            def __init__(self, url, params=None):
                self.status_code = 200
                
            def json(self):
                return {
                    "results" : [
                        {
                            "address_components" : [
                                                    {
                                                    "long_name" : place
                                                    }]}]}
        
        
        monkeypatch.setattr('flaskr.models.requests.get', MockRequestGet)
        GoogleApi().send_request("Paris")
       
        assert GoogleApi().send_request("Paris") == results
    
    
    def test_get_formatted_address:
        pass
    
    
class TestWikiApi:
    pass
    
    
class TestParser:
    pass