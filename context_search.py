

def removekaro(input_string):
    return input_string.replace(",", "")

def parse_search_results(input_string: str,results) -> list:
    # print(results)
    colon_index = input_string.rfind(":")

    if colon_index != -1:
        names_string = input_string[colon_index + 1:]
    else:
        names_string = input_string

    names = [name.strip() for name in names_string.split(",")]

    results_list = names[:20]
    
    res = []

    for result in results_list:
        try :
            res.append(results[result])
        except :
            print('oops')
    return res


def context_search(input_keyword,model,llm,es,indexName):
    
    # model = SentenceTransformer('all-mpnet-base-v2')
    vector_of_input_keyword = model.encode(input_keyword)

    
    query = {
            "field": "embeddings",
            "query_vector": vector_of_input_keyword,
            "k": 100,
            "num_candidates": 1000,
            
        }
    res = es.knn_search(index=indexName
                            , knn=query 
                            , source=["fullName","search_text","br_nm","secondary_category","_id"]
                            )
    results = res["hits"]["hits"]

    data_for_llama3 = {}
    appended_string = ""

    for hit in results:
        full_name = removekaro(hit["_source"]["fullName"])
        full_name = full_name.strip()
        data_for_llama3[str(hit["_id"])] = hit
        appended_string += full_name + " " + hit["_id"] + ", " 

    appended_string = appended_string[:-2]  

    llama3_prompt = f"Select the 20 best options from the given options to the question '{input_keyword}':\n{appended_string} just give out the ID which is mentioned just before a comma give them out in a single separated by commas"
    # print(llama3_prompt)
    # llm = Ollama(model="llama3")
    res = llm.invoke(llama3_prompt)
    # print(res)
    ans = parse_search_results(res,data_for_llama3)
    values = []
    for result in ans:
        values.append(result['_id'])
    query = {
  "query": {
    "bool": {
      
      "must": [
        { "ids": { "values":values } }
      ]
    }
  }
}
    res = es.search(index="hkdata1", body=query, size=10)
    final_ans = res["hits"]["hits"]
    print("Displayed LLM results")
    return final_ans
    

  