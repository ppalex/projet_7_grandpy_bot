from flaskr.models import GoogleApi, WikiApi, Response, Parser, Message


def treat_data_from_user(data):

    message = parse_data_from_user(data)
    google_api_data = get_data_from_google_api(message)
    
    if (google_api_data.get_status() == 'OK'):
        wiki_api_data, page_id = get_data_from_wiki_api(google_api_data)
        extract_text_from_wiki = wiki_api_data.get_extract(page_id)

        data_wiki = parse_data_from_wiki(extract_text_from_wiki)
        response_address = get_message_for_adress(
        ) + " " + google_api_data.get_formatted_address()

        response = Response(google_api_data.get_status(),
                            google_api_data.get_latitude(),
                            google_api_data.get_longitude(),
                            wiki_api_data.get_wiki_url(page_id),
                            response_address,
                            data_wiki,
                            None)
    else:
        response = Response(google_api_data.get_status(),
                            None,
                            None,
                            None,
                            None,
                            None,
                            get_message_for_error())

    return response.formatted_response()


def parse_data_from_user(data):
    parser = Parser(data)
    parser.set_lowercase()
    parser.remove_accents()
    parser.remove_stop_words()
    parser.remove_apostrof()
    parser.extract_questions()

    return parser.message


def parse_data_from_wiki(data):
    parser = Parser(data)
    section = parser.get_section()

    return section


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


def get_message_for_adress():
    data_message = Message.get_answers_from_json()
    return data_message.get_message_for_address()


def get_message_for_error():
    data_message = Message.get_answers_from_json()
    return data_message.get_message_for_error()
