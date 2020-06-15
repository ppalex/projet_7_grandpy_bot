from flaskr.models import GoogleApi


def treat_data_(data):
    
    google_api = GoogleApi()    
    google_api_response = google_api.send_request(data)
    
    return google_api_response