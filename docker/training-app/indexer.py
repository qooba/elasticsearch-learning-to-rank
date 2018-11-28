import json
import time
import sys
from utils import Elasticsearch, ES_INDEX, ES_TYPE, ES_DATA

class Indexer:

    def __init__(self, es: Elasticsearch):
        self.__es = es

    def prepare(self):
        try:
            print('Elasticsearch is alive',file=sys.stderr)
            with open(ES_DATA) as data:
                movieDict = json.loads(data.read())
                self.__reindex(self.__es, movieDict=movieDict, index=ES_INDEX, es_type=ES_TYPE)
        except:
            print('Upps ... wating for elasticsearch')
            time.sleep(5)
            self.prepare()  

        return "Index prepared, now prepare labels"

    def __enrich(self, movie):
        """ Enrich for search purposes """
        if 'title' in movie:
            movie['title_sent'] = 'SENTINEL_BEGIN ' + movie['title']

    def __bulkDocs(self, movieDict, index, es_type):
            for id, movie in movieDict.items():
                if 'release_date' in movie and movie['release_date'] == "":
                    del movie['release_date']
                self.__enrich(movie)
                addCmd = {"_index": index,
                          "_type": es_type,
                          "_id": id,
                          "_source": movie}
                yield addCmd
                if 'title' in movie:
                    print("%s added to %s" % (movie['title'], index),file=sys.stderr)

    def __reindex(self, es, analysisSettings={}, mappingSettings={}, movieDict={}, index='tmdb', es_type='movie'):
        import elasticsearch.helpers
        settings = {
            "settings": {
                "number_of_shards": 1,
                "index": {
                    "analysis" : analysisSettings,
                }}}

        if mappingSettings:
            settings['mappings'] = mappingSettings

        es.indices.delete(index, ignore=[400, 404])
        es.indices.create(index, body=settings)
        elasticsearch.helpers.bulk(es, self.__bulkDocs(movieDict, index, es_type))