from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch('https://localhost:9200')

doc = {
    'author': 'author_name',
    'text': 'Interensting content...',
    'timestamp': datetime.now(),
}
print ( doc)
print(es.get("tweet","1"))
#resp = es.index("test-index", 1, doc)
#print(resp['result'])