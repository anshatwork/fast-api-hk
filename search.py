

def search(es,input_keyword,page,indexName):
    
    query = {
        "query": {
            "multi_match": {
                "query": input_keyword,
                "fields": ["fullName", "search_text", "br_nm"],
                "minimum_should_match": "90%"
            }
        },
        "from" : page*10,
        "size": 10
    }
   
    res = es.search(index=indexName, body=query)
    results = res["hits"]["hits"]
    
    return results

def fuzzy_search(input_keyword, page,es,indexName):

    query = {
        "query": {
            "multi_match": {
                "query": input_keyword,
                "fields": ["fullName", "search_text", "br_nm"],
                "minimum_should_match" : "80%",
                "fuzziness" : 2

            }
        },
        "from" : page*10,
        "size" : 10
    }
    
    res = es.search(index=indexName, body=query)
    results = res["hits"]["hits"]
    print("ran fuzzy_query with page no " + str(page) + " for the query " + input_keyword)
    return results
