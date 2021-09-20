import spacy_streamlit
import streamlit as st
import spacy
from pathlib import Path
import srsly
import importlib
import random

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia**"""

# you have to load the model before we can add a pipe. This may be a problem.
# nlp = DEFAULT_MODEL.load()
NLP = spacy.load(DEFAULT_MODEL)

# set up custom NER Entity Ruler
ruler = NLP.add_pipe("entity_ruler", before='ner') # <- this is directly from spacy documentation

# Load the new pattern (list of custom entities) by adding them from the properly formatted jsonl file.
ruler.from_disk(Path(__file__).parent / "ansp-entity-ruler.jsonl")

def get_default_text(nlp):
    # Check if spaCy has built-in example texts for the language
    try:
        examples = importlib.import_module(f".lang.{nlp.lang}.examples", "spacy")
        return examples.sentences[0]
    except (ModuleNotFoundError, ImportError):
        return ""

# Get data to visualize
# from: https://share.streamlit.io/rtiinternational/rota-app 

st.markdown("**Upload Text File**")
uploaded_file = st.file_uploader("File Upload", type=["txt"])

if uploaded_file is not None:
    doc = spacy_streamlit.process_text(NLP, uploaded_file.getvalue().decode("utf-8"))

    spacy_streamlit.visualize(
        MODELS,
        doc,
        default_model=DEFAULT_MODEL,
        visualizers=["parser", "ner", "tokens"],
        show_visualizer_select=True,
        sidebar_description=DESCRIPTION,
    )
else:
    text = st.text_area("Text to analyze", DEFAULT_TEXT, height=200)
    doc = spacy_streamlit.process_text(nlp, text)
    
    spacy_streamlit.visualize(
        MODELS,
        default_model=DEFAULT_MODEL,
        visualizers=["parser", "ner", "tokens"],
        show_visualizer_select=True,
        sidebar_description=DESCRIPTION,
        # get_default_text=get_default_text
    )
