import json
import time
import sys
import os
from utils import Elasticsearch, ES_INDEX, ES_TYPE, ES_DATA, ES_HOST, ES_AUTH, ES_MODEL_NAME

class Tester:

    def __init__(self, es: Elasticsearch):
        self.__es = es

    def test(self, query):
        results = self.__es.search(index=ES_INDEX, doc_type=ES_TYPE, body=self.ltrQuery(query, ES_MODEL_NAME))
        res = []
        for result in results['hits']['hits']:
            res.append({'name': result['_source']
                        ['title'], 'id': result['_id'], 'score': result['_score']})

        return json.dumps(res)

    def ltrQuery(self, keywords, modelName):
        baseQuery = {
          "query": {
              "multi_match": {
                  "query": "test",
                  "fields": ["title", "overview"]
               }
           },
          "rescore": {
              "query": {
                "rescore_query": {
                    "sltr": {
                        "params": {
                            "keywords": ""
                        },
                        "model": "",
                    }
                 }
              }
           }
        }

        baseQuery['rescore']['query']['rescore_query']['sltr']['model'] = modelName
        baseQuery['query']['multi_match']['query'] = keywords
        baseQuery['rescore']['query']['rescore_query']['sltr']['params']['keywords'] = keywords
        print("%s" % json.dumps(baseQuery),file=sys.stderr)
        return baseQuery