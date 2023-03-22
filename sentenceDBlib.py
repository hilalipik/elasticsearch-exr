from elasticsearch import Elasticsearch
INDEX_NAME = "sentence-db"

es = Elasticsearch(["https://localhost:9200"], basic_auth=('elastic', 'I+MKSmMOkyeXaMNA8Gpb'), ca_certs="/Users/hilalipik/fionic_internship/elasticsearch-exr/http_ca.crt")

def delete_db():
    es.indices.delete(index=INDEX_NAME)

def init_db():
    '''
    Initializes data base if needed.
    '''
    if not es.indices.exists(index=INDEX_NAME):
        mappings = {
            "properties": {
                "sentence": {"type": "text"} #, "analyzer": "standard"}
            }
        }
        es.indices.create(index=INDEX_NAME, mappings=mappings)

def extract_sentences(res : "ObjectApiResponse") -> list[str]:
    '''
    Extract only the sentences from a elasticsearch response.
    Input: response.
    Output: a list of all sentences in the response.
    '''
    sentence_list = []
    res = res['hits']['hits']
    for sentence in res:
        sentence_list.append(sentence['_source']['sentence'])
    return sentence_list

def write(sentence : str) -> str:
    '''
    Writes a sentence to the elasticsearch DB.
    Input: sentence to add.
    Output: the result from elasticsearch.
    '''
    sentence_count = len(get_all()) # start adding sentences at the end
    doc = ({"sentence" : sentence})

    resp = es.index(index=INDEX_NAME, document=doc)
    return resp['result']

def get_all() -> list[str]:
    '''
    Returs all of the entries from DB
    Output: a list of all the sentences
    '''
    es.indices.refresh(index=INDEX_NAME)
    b = {"match_all": {}}
    res = es.search(index=INDEX_NAME, query=b)
    return extract_sentences(res)

def get_containing(word : str) -> list[str]:
    '''
    Gets all sentences from DB which contain a wanted word
    Input: word to search.
    Output: a list of all sentences from DB which contain the word.
    '''
    res = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "bool": {
                    "must": {
                        "match": {"sentence": word}
                    },
                    "filter": {"bool": {"must_not": {"match_phrase": {"director": "roman polanski"}}}},
                },
            },            
        }
    )
    return extract_sentences(res)

init_db()