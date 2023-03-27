from elasticsearch import Elasticsearch

class DBHandle:
    def __init__(self, db_name : str):
        '''
        Initializer, connects to db and creates it if needed.
        Input: the desired database name.
        '''
        self._INDEX_NAME = db_name
        self._es = Elasticsearch("http://localhost:9200")
        self._init_db()


    def delete_db(self):
        '''
        Deletes the database.
        '''
        self._es.indices.delete(index=self._INDEX_NAME)

    def _init_db(self):
        '''
        Initializes data base if needed.
        '''
        if not self._es.indices.exists(index=self._INDEX_NAME):
            mappings = {
                "properties": {
                    "sentence": {"type": "text"}
                }
            }
            self._es.indices.create(index=self._INDEX_NAME, mappings=mappings)

    def _extract_sentences(self, res : dict) -> list[str]:
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

    def write(self, sentence : str):
        '''
        Writes a sentence to the elasticsearch DB.
        Input: sentence to add.
        '''
        doc = ({"sentence" : sentence})

        res = self._es.index(index=self._INDEX_NAME, document=doc)

    def get_all(self) -> list[str]:
        '''
        Returns all of the entries from DB
        Output: a list of all the sentences
        '''
        self._es.indices.refresh(index=self._INDEX_NAME)
        res = self._es.search(index=self._INDEX_NAME, query={"match_all": {}})
        return self._extract_sentences(res)

    def get_containing(self, word : str) -> list[str]:
        '''
        Gets all sentences from DB which contain a wanted word
        Input: word to search.
        Output: a list of all sentences from DB which contain the word.
        '''
        self._es.indices.refresh(index=self._INDEX_NAME)
        res = self._es.search(
            index=self._INDEX_NAME,
            body={
                "query": {
                    "bool": {
                        "must": {
                            "match": {"sentence": word}
                        }
                    },
                },            
            }
        )
        return self._extract_sentences(res)
