from flaskr.models import GoogleApi, Response


def treat_data(data):
    
    google_api = GoogleApi()    
    google_api.send_request(data)
    
    response = Response(google_api.get_formatted_address(),
                        google_api.get_latitude(),
                        google_api.get_longitude(),
                        "",
                        "")   
    
    
    return response.formatted_response()