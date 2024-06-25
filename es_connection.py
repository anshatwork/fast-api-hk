from elasticsearch import Elasticsearch

def get_es_connection():
    try:
        es = Elasticsearch("http://localhost:9200/")
        if es.ping():
            print('successfully connected to es')
            return es
        else:
            print("Oops! Cannot connect to Elasticsearch!")
    except ConnectionError as e:
        print(f"Connection Error: {e}")
        return None
