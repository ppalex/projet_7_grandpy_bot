from flaskr.models import GoogleApi, WikiApi, Response, Parser


def treat_data_from_user(data):

    message = parse_data_from_user(data)
    google_api_data = get_data_from_google_api(message)
    wiki_api_data, page_id = get_data_from_wiki_api(google_api_data)
    
    response = Response(google_api_data.get_latitude(),
                        google_api_data.get_longitude(),
                        google_api_data.get_formatted_address(),
                        wiki_api_data.get_extract(page_id))

    return response.formatted_response()

def parse_data_from_user(data):
    parser = Parser(data)
    parser.set_lowercase()
    parser.remove_accents()
    parser.extract_questions()
    parser.remove_stop_words()
    parser.test_remove_apostrof()
    
    return parser.message


def get_data_from_google_api(data):

    google_api = GoogleApi()
    google_api.send_request(data)    

    return google_api


def get_data_from_wiki_api(data):

    latitude = data.get_latitude()
    longitude = data.get_longitude()

    geosearch_data = WikiApi()
    geosearch_data.send_geosearch_request(latitude, longitude)

    page_id = geosearch_data.get_page_id()

    pageids_data = WikiApi()
    pageids_data.send_pageids_request(page_id)

    return pageids_data, page_id
