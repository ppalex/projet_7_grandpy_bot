import logging
import requests

import configuration.config as config

config.load('./configuration/config.yml')

class GoogleApi:
    def __init__(self):
        self.url = config.value['GOOGLE']['URL']
        self.api_key = config.value['GOOGLE']['API_KEY']
        self.data = []
    
    
    def send_request(self, place):
        
        url = self.url + place + f"&key={self.api_key}"
        
        try:
            response = requests.get(url)
        except requests.exceptions.Timeout:
            logging.error("Timeout error")
        except requests.exceptions.TooManyRedirects:
            logging.error("Bad url")
        except requests.exceptions.RequestException as e:
            logging.error("Bad request")
            raise SystemExit(e)
            
        
        if response.status_code == 200:
            self.data = response.json()
        
        return self.data
    
    
    def get_formatted_adress:
        pass
        
        
    
class WikiApi:
    def __init__(self):
        pass
    
    
class Parser:
    def __init__(self):
        pass