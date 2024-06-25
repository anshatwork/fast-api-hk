import requests
import json
import streamlit as st

def display_results(results):
    st.subheader("Search Results")
    for result in results:
        with st.container():
            
                try:
                    st.header(f"{result['_source']['fullName']}")
                except Exception as e:
                    print(e)
                
                try:
                    st.write(f"Description: {result['_source']['secondary_category']}")
                except Exception as e:
                    print(e)
                st.divider()

def fetch_results(search_query, page):
    payload = {
        "query": search_query,
        "page": page
    }
    res = requests.post(url="http://127.0.0.1:8000/search", json=payload)
    response = res.json()
    results = response.get("results", [])
    return results

def fetch_total(search_query):
    payload = {
        "query" : search_query
    }
    res = requests.post(url="http://127.0.0.1:8000/total", json=payload)
    response = res.json()
    results = response.get("results", [])
    return len(results)

def fetch_llm_results(search_query):
    payload = {
        "query" : search_query
    }
    res = requests.post(url="http://127.0.0.1:8000/contextSearch", json=payload)
    response = res.json()
    results = response.get("results", [])
    return results

def main():
    st.title("Search at HealthKart")

    search_query = st.text_input("Enter your search query")

    if st.button("Search"):
        st.session_state.search_query = search_query
        st.session_state.page_number = 0
        st.session_state.results = fetch_results(st.session_state.search_query, st.session_state.page)
        st.session_state.total = fetch_total(st.session_state.search_query)
        st.session_state.context_results = fetch_llm_results(st.session_state.search_query)
        print((str)(st.session_state.total) + " non LLM results ")
        print(len(st.session_state.context_results))

    if st.session_state.search_query:
            
            N = 10
        
            last_page = 2+  (st.session_state.total//N) 
            
            prev, _ ,next = st.columns([5, 10, 5])

            st.session_state.check = 0

            if st.session_state.page_number < last_page :
                if next.button("Next"):
                    st.session_state.page_number += 1

            if st.session_state.page_number > 0 :
                if prev.button("Previous"):          
                    st.session_state.page_number -= 1

            if st.session_state.page_number > last_page -3:
                st.subheader("LLM results")
                if st.session_state.page_number == last_page-2:
                    display_results(st.session_state.context_results[:N+st.session_state.check])    
                else : display_results(st.session_state.context_results[N+st.session_state.check:])
            else :
                results = fetch_results(st.session_state.search_query,st.session_state.page_number)
                display_results(results)

if __name__ == "__main__":
    main()
    