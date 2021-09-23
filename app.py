import spacy_streamlit
import streamlit as st
import spacy
from pathlib import Path
import srsly
import importlib
import random
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities
from spacy.language import Language  # type: ignore 
import json

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. Seven Ampelis cedrorum specimens were collected in a meadow near lowland fruit trees. Some habitats we know are in the json file are near large rocks, near river mouths, near the bottom and near the ocean. Some species names are Hemigrapsus affinis, Hemigrapsus crassimanus, Hendersonia alternifoliae and Hendersonia celtifolia."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia**"""

# functions to create the custom entity ruler
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

#taxa_patterns = create_training_data("streamlit-ansp/ansp-taxa.json", "TAXA")
#hab_patterns = create_training_data("streamlit-ansp/ansp-habitat.json", "HABITAT")

def generate_rules(patterns):
    nlp = spacy.load(DEFAULT_MODEL)
    # ruler = EntityRuler(nlp)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.add_patterns(patterns)
    # nlp.add_pipe(ruler)
    nlp.to_disk("ansp_ner")
    
# FILE UPLOADER
st.markdown("**Upload Text File**")
uploaded_file = st.file_uploader("File Upload", type=["txt"])

if uploaded_file is not None:
    patterns = srsly.read_json(Path(__file__).parent / "ansp-entity-ruler.json")
    generate_rules(patterns)
    doc = nlp(uploaded_file.getvalue().decode("utf-8"))
    
    spacy_streamlit.visualize(
        doc,
        MODELS,
        default_model=DEFAULT_MODEL,
        visualizers=["parser", "ner", "tokens"],
        show_visualizer_select=True,
        sidebar_description=DESCRIPTION,
    )

# IF NO FILE UPLOADED
else:
    # you have to load the model before we can add a pipe. This may be a problem?
    #NLP = spacy.load(DEFAULT_MODEL)
    # set up custom NER Entity Ruler
    #ruler = NLP.add_pipe("entity_ruler", before='ner') # <- this is directly from spacy documentation
    # Load the new pattern (list of custom entities) by adding them from the properly formatted jsonl file.
    #ruler.from_disk(Path(__file__).parent / "ansp-entity-ruler.json")
    
    text = st.text_area("Text to analyze", DEFAULT_TEXT, height=200)
    # doc = spacy_streamlit.process_text(NLP, text)

    patterns = create_training_data("streamlit-ansp/ansp-taxa.json", "TAXA")
    generate_rules(patterns)
    nlp = spacy.load("ansp_ner")
    doc = nlp(text)
    
    spacy_streamlit.visualize(
        MODELS,
        doc,
        default_model=DEFAULT_MODEL,
        visualizers=["parser", "ner", "ansp_ner", "tokens"],
        show_visualizer_select=True,
        sidebar_description=DESCRIPTION,
    )