import spacy
from pathlib import Path
import srsly
import importlib
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities
from spacy.language import Language  # type: ignore 
import json

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def create_training_data(file, type):
    data = load_data(file) 
    patterns = []
    for item in data:
        pattern = {
                    "label": type,
                    "pattern": item
                    }
        patterns.append(pattern)
    return (patterns)

taxa_patterns = create_training_data("streamlit-ansp/ansp-taxa.json", "TAXA")
hab_patterns = create_training_data("streamlit-ansp/ansp-habitat.json", "HABITAT")
  
nlp = spacy.load("en_core_web_sm")
ruler = nlp.add_pipe("entity_ruler", before='ner')
ruler.add_patterns(taxa_patterns)
ruler.add_patterns(hab_patterns)

ruler.to_disk("streamlit-ansp/ansp-patterns.jsonl")