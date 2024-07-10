from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import spacy
import requests
import re

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

roxie_url = "http://university-roxie.us-hpccsystems-dev.azure.lnrsg.io:8002/WsEcl/json/query/roxie/roxie_index_search_2"

# Roxie server Authorization header
roxie_auth_header = {
    'Authorization': 'Basic bWFudml0aGxiOmt6bzZmVW5lNWRTU0h6Y2o='
}

# Load the legal NER model
nlp = spacy.load("en_legal_ner_sm")

@app.route('/')
def index():
    return "Welcome to the backend API!"

@app.route('/process_text', methods=['POST'])
@cross_origin()  # This decorator automatically adds the Access-Control-Allow-Origin header
def process_text():
    data = request.get_json()
    text = data.get('text', '')

    # Process the text with the legal NER model
    doc = nlp(text)

    # Extract identified entities
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents if ent.label_ in {'COURT', 'PROVISION', 'STATUTE'}]
    # Print entities and their labels to the console
    for entity in entities:
        print(f"Entity: {entity['text']}, Label: {entity['label']}")

    # Combine adjacent provisions and statutes, and remove the year from statutes
    combined_entities = []
    i = 0
    while i < len(entities):
        current_entity = entities[i]
        if current_entity['label'] == 'PROVISION' and i + 1 < len(entities) and entities[i + 1]['label'] == 'STATUTE':
            statute_text = re.sub(r'\b\d{4}\b', '', entities[i + 1]['text']).strip()
            combined_text = f"{current_entity['text']} {statute_text}"
            combined_entities.append({'text': combined_text, 'label': 'PROVISION_STATUTE'})
            i += 2  # Skip the next entity as it is already combined
        elif current_entity['label'] in {'COURT', 'PRECEDENT'}:
            combined_entities.append(current_entity)
            i += 1
        else:
            i += 1  # Skip standalone STATUTE or PROVISION

    # Prepare the keywords string with commas
    keywords = ", ".join([ent['text'] for ent in combined_entities])

    return jsonify({"entities": combined_entities, "keywords": keywords})


@app.route('/sendroxie', methods=['POST'])
@cross_origin()
def send_roxie():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    data = request.get_json()
    keywords = data.get('keywords', '')

    print(keywords)

    try:
        payload = {
             "roxie_index_search_2": {
               "enter_words_separated_by_forward_slash": keywords
            }
        }

        headers = {
            "Content-Type": "application/json",
            **roxie_auth_header
        }
        
        
        response = requests.post(roxie_url, json=payload, headers=headers)
        # print("Response Status Code:", response.status_code)
        # print("Response Headers:", response.headers)
        # print("Response JSON:", response.json())
        roxie_data = response.json()
        return jsonify(roxie_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
