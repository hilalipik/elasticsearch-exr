from elasticsearch import Elasticsearch

es = Elasticsearch(["https://localhost:9200"], basic_auth=('elastic', 'I+MKSmMOkyeXaMNA8Gpb'), ca_certs="/Users/hilalipik/fionic_internship/elasticsearch-exr/http_ca.crt")
sentence_counter=0
def write(sentence : str) -> str:
    '''
    writes a sentence to the elasticsearch DB.
    Input: sentence to add.
    Output: the result from elasticsearch.
    '''
    global sentence_counter
    doc = {
        'sentence': sentence
    }

    resp = es.index(index=sentence_counter, id=sentence_counter, document=doc)
    sentence_counter +=1
    return resp['result']

def get_all() -> list[str]:
    '''
    Returs all of the entries from DB
    Output: a list of all the sentences
    '''
    sentences = []
    for index in es.indices.get(index='*'):
        sentences+= es.get(index=index, id=index)['_source'].values()
    return sentences

def get_containing(word : str) -> list[str]:
    '''
    Gets all sentences from DB which contain a wanted word
    Input: sentence to add.
    Output: the result from elasticsearch.
    '''
    all_sentences = get_all()
    containing=[]
    for sentence in all_sentences:
        if word in sentence:
            containing.append(sentence)
    return containing

sentence_counter = len(get_all()) # start adding sentences at the end