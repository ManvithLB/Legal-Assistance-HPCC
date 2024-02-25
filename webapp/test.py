import spacy
from spacy.scorer import Scorer

# Default scoring pipeline
scorer = Scorer()

# Provided scoring pipeline
nlp = spacy.load("en_core_web_sm")
scorer = Scorer(nlp)