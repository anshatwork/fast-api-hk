from fastapi import FastAPI, Request
import uvicorn
from multiprocessing import Process
import subprocess
from es_connection import get_es_connection
from search import search
from total import search_count,fuzzy_search_count
from context_search import context_search
from entity import entity
from sentence_transformers import SentenceTransformer
from langchain_community.llms import Ollama

indexName = "hkdata1"
rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
model = SentenceTransformer('all-mpnet-base-v2')

llm = Ollama(model = "llama3")

app = FastAPI()
es = get_es_connection()

@app.post("/total")
async def total_endpoint(request: Request):
    json_data = await request.json()
    search_query = json_data.get("query")
    
    
    if es:
        results = search_count( search_query,es,indexName)
        # if results == 0:
        #     results = fuzzy_search_count(es,search_query,indexName)
        # print(results)
        return {"results": results}
    else:
        # print('hello world')
        return {"error": "Could not connect to Elasticsearch"}


@app.post("/search")
async def search_endpoint(request: Request):
    json_data = await request.json()
    search_query = json_data.get("query")
    page = json_data.get("page")
    
    if es:
        results = search(es, search_query,page,indexName)
        # print(results)
        return {"results": results}
    else:
        # print('hello world')
        return {"error": "Could not connect to Elasticsearch"}
    
@app.post("/contextSearch")
async def context_search_endpoint(request: Request):
    json_data = await request.json()
    search_query = json_data.get("query")
    
    
    if es:
        results = context_search( search_query,model,llm,es,indexName)
        # print(results)
        return {"results": results}
    else:
        # print('hello world')
        return {"error": "Could not connect to Elasticsearch"}

@app.post("/getEntity")
async def context_search_endpoint(request: Request):
    json_data = await request.json()
    search_query = json_data.get("query")
    
    
    if es:
        results = entity( search_query,rasa_server_url)
        # print(results)
        return {"results": results}
    else:
        
        return {"error": "Could not connect to Elasticsearch"}


# def run_streamlit():
#     subprocess.run(["streamlit", "run", "display.py"])

if __name__ == "__main__":
    # Run Streamlit in a separate process
    # p = Process(target=run_streamlit)
    # p.start()

    # Run FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # Join Streamlit process to prevent the script from terminating
    # p.join()
