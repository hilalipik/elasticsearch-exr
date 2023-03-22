from elasticsearch import Elasticsearch

class dbHandle:
    def __init__(self, db_name):
        self.__INDEX_NAME__ = db_name
        self.__es__ = Elasticsearch(["http://localhost:9200"])
        self.__init_db__()


    def __delete_db__(self):
        self.__es__.indices.delete(index=self.__INDEX_NAME__)

    def __init_db__(self):
        '''
        Initializes data base if needed.
        '''
        if not self.__es__.indices.exists(index=self.__INDEX_NAME__):
            mappings = {
                "properties": {
                    "sentence": {"type": "text"} #, "analyzer": "standard"}
                }
            }
            self.__es__.indices.create(index=self.__INDEX_NAME__, mappings=mappings)

    def __extract_sentences__(self, res : "ObjectApiResponse") -> list[str]:
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

        res = self.__es__.index(index=self.__INDEX_NAME__, document=doc)
        return res['result']

    def get_all(self) -> list[str]:
        '''
        Returs all of the entries from DB
        Output: a list of all the sentences
        '''
        self.__es__.indices.refresh(index=self.__INDEX_NAME__)
        res = self.__es__.search(index=self.__INDEX_NAME__, query={"match_all": {}})
        return self.__extract_sentences__(res)

    def get_containing(self, word : str) -> list[str]:
        '''
        Gets all sentences from DB which contain a wanted word
        Input: word to search.
        Output: a list of all sentences from DB which contain the word.
        '''
        res = self.__es__.search(
            index=self.__INDEX_NAME__,
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
        return self.__extract_sentences__(res)

