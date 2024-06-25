
def search_count(input_keyword,es,indexName):

    query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": input_keyword,
                        "fields": ["fullName", "search_text", "br_nm"],
                        "minimum_should_match": "90%"
                    }
                }
                
            }
        },
        
        "size": 40
    }
    res = es.search(index=indexName, body=query)
    results = res["hits"]["hits"]
    
    return (results)

def fuzzy_search_count(input_keyword,es,indexName):

    query = {
        "query": {
            "multi_match": {
                "query": input_keyword,
                "fields": ["fullName", "search_text", "br_nm"],
                "minimum_should_match": "80%",
                "fuzziness" : 2
            }
        },
        
        "size" : 40
    }
    
    res = es.search(index=indexName, body=query)
    results = res["hits"]["hits"]
    return (results)