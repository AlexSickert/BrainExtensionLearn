from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

"""

https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/

http://elasticsearch-py.readthedocs.io/en/master/api.html?highlight=search

https://elasticsearch-py.readthedocs.io/en/master/

"""

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool.  xxxx  bonsai cool.',
    'myfield' : "the brown fox jumps...",
    'timestamp': datetime.now(),
}
res = es.index(index="test-index", doc_type='tweet', id=111, body=doc)

print(res)


print(res['result'])

res = es.get(index="test-index", doc_type='tweet', id=1)
print(res['_source'])

es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
res = es.search(index="test-index", body={"query": {"match": {"myfield" : "fox"}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s %(myfield)s" % hit["_source"])