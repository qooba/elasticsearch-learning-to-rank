import os
import json
import elasticsearch
from requests.auth import HTTPBasicAuth

__all__ = ["ES_AUTH", "ES_HOST", "ES_INDEX", "ES_TYPE", "ES_DATA", "ES_FEATURE_SET_NAME", "ES_MODEL_TYPE", "ES_METRIC_TYPE", "Elasticsearch"]

ES_HOST = os.environ['ES_HOST']
ES_USER = os.environ.get('ES_USER', None)
ES_PASSWORD = os.environ.get('ES_PASSWORD', None)
ES_INDEX = os.environ.get('ES_INDEX', 'tmdb')
ES_TYPE = os.environ.get('ES_TYPE', 'movie')
ES_DATA = os.environ.get('ES_DATA', '/opt/services/flaskapp/tmdb.json')
ES_FEATURE_SET_NAME = os.environ.get('ES_FEATURE_SET_NAME', 'movie_features')
ES_MODEL_NAME = os.environ.get('ES_MODEL_NAME', 'test_6')
ES_MODEL_TYPE = os.environ.get('ES_MODEL_TYPE', '6')
ES_METRIC_TYPE = os.environ.get('ES_METRIC_TYPE', 'ERR@10')

if ES_USER is not None and ES_PASSWORD is not None:
    auth = (ES_USER, ES_PASSWORD)
    ES_AUTH = HTTPBasicAuth(*auth)
else:
    auth = None
    ES_AUTH = None


def Elasticsearch(url=None, timeout=1000, http_auth=auth):
    if url is None:
        url = ES_HOST

    return elasticsearch.Elasticsearch(url, timeout=timeout, http_auth=http_auth)
