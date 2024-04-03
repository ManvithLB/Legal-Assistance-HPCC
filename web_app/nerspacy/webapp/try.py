from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin
import spacy
import requests

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

# Load the legal NER model
nlp = spacy.load("en_legal_ner_sm")

# Roxie server URL
roxie_url = "http://university-roxie.us-hpccsystems-dev.azure.lnrsg.io:8002/WsEcl/json/query/roxie/legal_roxie_search_2"

# Roxie server Authorization header
roxie_auth_header = {
    'Authorization': 'Basic bWFudml0aGxiOmt6bzZmVW5lNWRTU0h6Y2o='
}

@app.route('/')
def index():
    return "Welcome to the backend API!"


@app.route('/process_text', methods=['POST'])
@cross_origin()  # This decorator automatically adds the Access-Control-Allow-Origin header
def process_text():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    data = request.get_json()
    text = data.get('text', '')

    # Process the text with the legal NER model
    doc = nlp(text)

    # Extract identified entities
    entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]

    # Prepare the keywords string with commas
    keywords = ", ".join([ent['text'] for ent in entities])

    # Prepare the JSON payload for the Roxie server
    payload = {
        "legal_roxie_search": {
            "enter_words_with_comma": keywords
        }
    }

    # Set the headers
    headers = {
        "Content-Type": "application/json",
        **roxie_auth_header  # Include Roxie server Authorization header
    }

    # Make a POST request to the Roxie server
    response = requests.post(roxie_url, json=payload, headers=headers)

    # print("Received JSON response:")
    # print(response.text)

    # Check the response from the Roxie server
    if response.status_code == 200:
        # Return the response from the Roxie server as JSON
        return response.json()
    else:
        # Return an error message if the request to Roxie fails
        return jsonify({"error": f"Failed to connect to Roxie server. Status Code: {response.status_code}"}), 500

    
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
