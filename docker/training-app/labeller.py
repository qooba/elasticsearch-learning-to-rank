import json
import time
import sys
from utils import Elasticsearch, ES_INDEX, ES_TYPE, ES_DATA


class Labeller:

    def __init__(self, es: Elasticsearch):
        self.__es = es

    def prepare_labels(self):
        with open('label_list.json') as f:
            return f.read()

    def search(self, query):
        search_query = {
            "query": {
                "multi_match": {
                    "query": "test",
                    "fields": ["title", "overview"]
                }
            }
        }

        es = Elasticsearch()
        search_query["query"]["multi_match"]["query"] = query
        results = es.search(
            index=ES_INDEX, doc_type=ES_TYPE, body=search_query)

        res = []
        for result in results['hits']['hits']:
            res.append({'name': result['_source']
                        ['title'], 'id': result['_id']})

        return json.dumps(res)

    def save(self, labels):
        ts = str(int(time.time()))
        with open('{}_judgments.txt'.format(ts), 'w') as f:
            f.write('# grade (0-4)	queryid	docId	title\n')
            f.write('# \n')
            f.write('# Add your keyword strings below, the feature script will \n')
            f.write('# Use them to populate your query templates \n')
            f.write('# \n')
            for query in labels['queries']:
                f.write('# qid:{}: {}\n'.format(str(query['index']+1),query['query']))
            f.write('# \n')
            f.write('# https://sourceforge.net/p/lemur/wiki/RankLib%20File%20Format/\n')
            f.write('# \n')
            f.write('# \n')
            for rating in labels['ratings']:
                f.write('{} qid:{} # {} {}\n'.format(rating['rating'], str(rating['query_id']+1), rating['id'], rating['name']))

        return 'Labels saved, now train the model'
