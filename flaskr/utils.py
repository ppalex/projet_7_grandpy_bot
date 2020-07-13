from flaskr.models import GoogleApi, WikiApi, Response, Parser, Message


def treat_data_from_user(data):
    """This function treat the data send by the user. The data come from the
    form.

    Args:
        data (String): Contains the sentence introduced by the user
        in the form.

    Returns:
        [Response]: Contains the data from the google api and
        media wiki api + messages that will be shown to the
        user.
    """

    message = parse_data_from_user(data)
    google_api_data = get_data_from_google_api(message)
    
    if (google_api_data.get_status() == 'OK'):
        wiki_api_data, page_id = get_data_from_wiki_api(google_api_data)
        
        check_page_id(google_api_data, page_id)

        if (google_api_data.get_status() == 'OK'):

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
    """This function creates a parser with a string data. It applies the
    methods from the Parser class to clean the string.

    Args:
        data (String): Message from the user with uppercaser letters,
        apostrophes, questions and non question text parts.

    Returns:
        [String]: Contains only one questions that comes from the message.
    """
    parser = Parser(data)
    parser.set_lowercase()
    parser.remove_accents()
    parser.remove_apostrof()
    parser.remove_hyphen()
    parser.remove_stop_words()
    parser.extract_questions()

    return parser.message


def parse_data_from_wiki(data):
    """This method parse the text get from the wikipedia.

    Args:
        data (String): The entire page from wirkipedia for a place.

    Returns:
        [String]: Contains only one section from the page.
    """
    parser = Parser(data)
    section = parser.get_section()

    return section


def get_data_from_google_api(data):
    """This method creates a google api Object and send a request to the api
    endpoint.

    Returns:
        [Object]: GoogleApi contains data from api google.
    """
    google_api = GoogleApi()
    google_api.send_request(data)

    return google_api


def get_data_from_wiki_api(data):
    """This method creates a wiki api Object and send a request to the api
    endpoint.

    Args:
        data (JSON): Contains the response from the google map api.

    Returns:
        [Tuple]: Contains the response from the wiki api and the id
        of the page.
    """
    latitude = data.get_latitude()
    longitude = data.get_longitude()

    geosearch_data = WikiApi()
    geosearch_data.send_geosearch_request(latitude, longitude)

    page_id = geosearch_data.get_page_id()

    pageids_data = WikiApi()
    pageids_data.send_pageids_request(page_id)

    return pageids_data, page_id


def get_message_for_adress():
    """This method get the message that will be send with the address.

    Returns:
        [String]: Address.
    """
    data_message = Message.get_answers_from_json()
    return data_message.get_message_for_address()


def get_message_for_error():
    """This method get the message that will be send if the message text from
    the user can not be analysed.

    Returns:
        [String]: Error sentence.
    """
    data_message = Message.get_answers_from_json()
    return data_message.get_message_for_error()


def check_page_id(google_api, page_id):
    """This method check if the page_id is present in the request response from
    wiki. If there is no page_id, the status of the google_api is set to "NOT
    OK".

    Args:
        google_api (Object):
        page_id (Int): Page id of the wiki page.
    """
    if page_id is None:
        google_api.set_status("NOT OK")
        
