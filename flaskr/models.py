import logging
import requests

import Configuration.config as config

config.load('./configuration/config.yml')

class GoogleApi:
    def __init__(self):
        pass
    
    
    def get_localization(self, place):
        
        data = []
        url_google_map = config['GOOGLE']['URL']
        
        try:
            response = requests.get('url')
        except requests.exceptions.Timeout:
            logging.error("Timeout error")
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url")
        except requests.exceptions.RequestException as e:
            logging.error("Bad request")
            raise SystemExit(e)
            
        
        if response.status_code == 200:
            data = response.json()
        
        return data
        
        
    
class WikiApi:
    def __init__(self):
        pass
    
    
class Parser:
    def __init__(self):
        pass