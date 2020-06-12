from flaskr.models import GoogleApi

class TestGoogleApi: 
    
        
    def test_get_localization(self, monkeypatch):
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
        GoogleApi().get_localization("Paris")
       
        assert GoogleApi().get_localization("Paris") == results
    
    
    
    
class TestWikiApi:
    pass
    
    
class TestParser:
    pass