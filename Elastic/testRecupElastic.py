from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

ELASTIC_PASSWORD = "qnR5=oW1049d7byzbet0"
pathCert = "C:/Users/splanchenault/Desktop/elasticsearch-8.4.3/config/certs/http_ca.crt"
certificate = "d35db3c8313866065ca9a268001255d6da85af0ad1bb99c62d3f7ba8b9951b86"

es = Elasticsearch("http://localhost:9200")
contenuTweet = []


def scanId(index):
    hits = helpers.scan(
        es,
        query={"query": {"match_all": {}}},
        scroll='1m',
        index=index
    )
    ids = [hit['_id'] for hit in hits]
    return ids


def getText(index, ids):
    ids=ids[1:]
    for i in ids: # faut prendre le +1
        test = es.get(index=index, id=i)
        if 'text' in test['_source'] :
            contenuTweet.append(test['_source']['text'])
