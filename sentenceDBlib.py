from elasticsearch import Elasticsearch

es = Elasticsearch(["https://localhost:9200"], basic_auth=('elastic', 'I+MKSmMOkyeXaMNA8Gpb'), ca_certs="/Users/hilalipik/fionic_internship/elasticsearch-exr/http_ca.crt")
__sentence_counter__=0

def init_db():
    '''
    Initializes data base with one sentence.
    Ooutput:the result from elasticsearch.
    '''
    global __sentence_counter__

    doc = {0 : "Hello world!"}
    resp = es.index(index="sentence-db", id=0, document=doc)
    __sentence_counter__ = 1

    return resp['result']

def write(sentence : str) -> str:
    '''
    Writes a sentence to the elasticsearch DB.
    Input: sentence to add.
    Output: the result from elasticsearch.
    '''
    global __sentence_counter__

    doc = __get_all__()
    doc.update({__sentence_counter__: sentence})

    resp = es.index(index="sentence-db", id=0, document=doc)
    __sentence_counter__ +=1
    return resp['result']

def __get_all__() -> dict:
    '''
    Returs all of the entries from DB
    Output: a dictionary of all the sentences
    '''
    return es.get(index="sentence-db", id=0)['_source']

def get_all() -> list[str]:
    '''
    Returs all of the entries from DB
    Output: a list of all the sentences
    '''
    return list(__get_all__().values())
 
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

__sentence_counter__ = len(get_all()) # start adding sentences at the end
