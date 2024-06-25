import requests
import pandas as pd

def entity(query,rasa_server_url):
    
    payload_data = {
        "sender": "user123",
        "message": query
    }

    response = requests.post(rasa_server_url, json=payload_data)

    
    if response.status_code == 200:
        
        rasa_response = response.json()
        
        
        if rasa_response and len(rasa_response) > 0:
            bot_message = rasa_response[0].get('text', "No response received from Rasa.")

            print("Response from Rasa:", bot_message)
            bot_message
        else:
            print("No response received from Rasa.")
    else:
        print("Error:", response.status_code)

    result = parse_response(bot_message)
    return result


def getEntity():
    data = pd.read_csv('data.csv')

    # Ensure all entries are in lowercase
    data['_source.br_nm'] = data['_source.br_nm'].str.lower()
    data['_source.secondary_category'] = data['_source.secondary_category'].str.lower()

    unique_brands = data['_source.br_nm'].dropna().unique()
    unique_categories = data['_source.secondary_category'].dropna().unique()

    unique_brands_list = unique_brands.tolist()
    unique_categories_list = unique_categories.tolist()
    return unique_brands_list,unique_categories_list

def parse_response(response):
    # Split the response into the search query part and the information part
    parts = response.split("kramer")
    
    if len(parts) < 2:
        return "Invalid response format"
    
    search_query = parts[0].strip()
    info_part = parts[1].strip()
    
    brand_match = ""
    category_match = ""
    
    # Split the info part into words
    words = [word.strip() for word in info_part.split() if word.strip()]
    
    # Extract brand and category
    for i in range(len(words)):
        if words[i] == 'brand':
            i += 1
            while i < len(words) and words[i] != 'and':
                brand_match += words[i] + " "
                i += 1
        if i < len(words) and words[i] == 'category':
            i += 1
            while i < len(words):
                category_match += words[i] + " "
                i += 1
    
    brand_match = brand_match.strip()
    category_match = category_match.strip()
    
    brands,categories = getEntity() 

    if category_match.strip() == 'category':
        category_match = 'proteins'
    
    if brand_match.strip().lower() == 'optimum nutrition':
        brand_match = 'on'

    if category_match not in categories:
        category_match = None

    if brand_match not in brands:
        brand_match = None

    return search_query, brand_match, category_match
