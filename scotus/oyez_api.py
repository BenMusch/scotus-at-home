import pprint

import requests

BASE_URL = "https://www.oyez.org/"
BASE_API_URL = "https://api.oyez.org/"
BASE_SEARCH_URL = "https://beta-search.oyez.org/elasticsearch_index_scotus_nodes/_search"

def __get(path, base_url=BASE_API_URL):
    url = "{}{}".format(BASE_API_URL, path)
    return requests.get(url).json()

def search(keyword):
    """Returns the docket numbers corresponding with the given keyword"""
    data = { "size": 20, "query": {
        "multi_match": {
            "query": keyword,
            "type": "cross_fields",
            "fields":["field_docket_number^3","field_additional_docket_numbers^3","title^2","field_court_term","field_first_party","field_second_party"]}}}

    results = requests.post(BASE_SEARCH_URL, json=data).json()["hits"]["hits"]
    just_cases = filter(lambda obj: obj["_source"]["type"] == "case", results)
    docket_nums = list(map(lambda case: case["_source"]["field_docket_number"], just_cases))
    return docket_nums

def cases(term):
    path = "cases?filter=term:{}".format(term)
    return __get(path)

def case(term, docket_num):
    path = "cases/{}/{}".format(term, docket_num)
    return __get(path)
