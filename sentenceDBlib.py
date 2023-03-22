from elasticsearch import Elasticsearch

class dbHandle:
    def __init__(self, db_name):
        self.INDEX_NAME = db_name
        self.es = Elasticsearch(["http://localhost:9200"])
        self.init_db()


    def delete_db(self):
        self.es.indices.delete(index=self.INDEX_NAME)

    def init_db(self):
        '''
        Initializes data base if needed.
        '''
        if not self.es.indices.exists(index=self.INDEX_NAME):
            mappings = {
                "properties": {
                    "sentence": {"type": "text"} #, "analyzer": "standard"}
                }
            }
            self.es.indices.create(index=self.INDEX_NAME, mappings=mappings)

    def extract_sentences(self, res : "ObjectApiResponse") -> list[str]:
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

    def write(self, sentence : str) -> str:
        '''
        Writes a sentence to the elasticsearch DB.
        Input: sentence to add.
        Output: the result from elasticsearch.
        '''
        doc = ({"sentence" : sentence})

        res = self.es.index(index=self.INDEX_NAME, document=doc)
        return res['result']

    def get_all(self) -> list[str]:
        '''
        Returs all of the entries from DB
        Output: a list of all the sentences
        '''
        self.es.indices.refresh(index=self.INDEX_NAME)
        res = self.es.search(index=self.INDEX_NAME, query={"match_all": {}})
        return self.extract_sentences(res)

    def get_containing(self, word : str) -> list[str]:
        '''
        Gets all sentences from DB which contain a wanted word
        Input: word to search.
        Output: a list of all sentences from DB which contain the word.
        '''
        res = self.es.search(
            index=self.INDEX_NAME,
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
        return self.extract_sentences(res)

