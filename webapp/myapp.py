from flask import Flask, render_template, request, jsonify
import spacy

app = Flask(__name__)

# Load the legal NER model
nlp = spacy.load("en_legal_ner_sm")

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

    return jsonify(entities)

if __name__ == '__main__':
    app.run(debug=True)
