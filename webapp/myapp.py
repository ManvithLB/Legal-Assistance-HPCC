from flask import Flask, render_template, request, jsonify
import spacy
import requests
import json

app = Flask(__name__)

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
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form['text']

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

    # Print the sent JSON payload to the console
    print("Sent JSON payload:")
    print(json.dumps(payload, indent=2))

    # Make a POST request to the Roxie server
    response = requests.post(roxie_url, json=payload, headers=headers)

    # Print the received JSON response to the console
    print("Received JSON response:")
    print(response.text)

    # Check the response from the Roxie server
    if response.status_code == 200:
        # Return the response from the Roxie server as JSON
        return jsonify(response.json())
    else:
        # Return an error message if the request to Roxie fails
        return jsonify({"error": f"Failed to connect to Roxie server. Status Code: {response.status_code}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
