from flaskr.models import GoogleApi, WikiApi, Response


def treat_data_from_user(data):
    google_api_data = get_data_from_google_api(data)
    wiki_api_data = get_data_from_wiki_api(google_api_data)

    import pdb
    pdb.set_trace()

    return None


def get_data_from_google_api(data):

    google_api = GoogleApi()
    google_api.send_request(data)

    # response = Response(google_api.get_formatted_address(),
    #                     google_api.get_latitude(),
    #                     google_api.get_longitude(),
    #                     "",
    #                     "")

    return google_api


def get_data_from_wiki_api(data):

    latitude = data.get_latitude()
    longitude = data.get_longitude()

    geosearch_data = WikiApi()
    geosearch_data.send_geosearch_request(latitude, longitude)

    page_id = geosearch_data.get_page_id()

    pageids_data = WikiApi()
    pageids_data.send_pageids_request(page_id)

    return pageids_data
