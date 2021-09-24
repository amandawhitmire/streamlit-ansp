import spacy_streamlit
import streamlit as st
import spacy
from pathlib import Path
import srsly
import importlib
import random
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities
from spacy.language import Language  # type: ignore 

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. Seven Ampelis cedrorum specimens were collected in a meadow near lowland fruit trees. Some habitats we know are in the json file are near large rocks, near river mouths, near the bottom and near the ocean. Some species names are Hemigrapsus affinis, Hemigrapsus crassimanus, Hendersonia alternifoliae and Hendersonia celtifolia."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia**"""

# NOTE: custom patterns have already been created for the NLP Pipeline > Entity Ruler via the ruler.py file.
    
# FILE UPLOADER
st.markdown("**Upload Text File**")
uploaded_file = st.file_uploader("File Upload", type=["txt"])

if uploaded_file is not None:
    
    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(Path(__file__).parent / "ansp-patterns.jsonl")
    doc = nlp(uploaded_file.getvalue().decode("utf-8"))
    
    for ent in doc.ents:
        st.write(ent.text, ",", ent.label_)
    
    spacy_streamlit.visualize(
        MODELS,
        doc,
        default_model=DEFAULT_MODEL,
        visualizers=["parser", "ner", "tokens"],
        show_visualizer_select=True,
        sidebar_description=DESCRIPTION,
    )

# IF NO FILE UPLOADED
else:
    
    text = st.text_area("Text to analyze", DEFAULT_TEXT, height=200)

    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(Path(__file__).parent / "ansp-patterns.jsonl")
    doc = nlp(text)
    
    for ent in doc.ents:
        st.write(ent.text, ",", ent.label_)
    
    labels=list(nlp.get_pipe("ner").labels)
    for label in nlp.get_pipe("entity_ruler").labels:
        labels.append(label)
        
    spacy_streamlit.visualize_ner(doc, labels=labels)
    
    #spacy_streamlit.visualize(
    #    MODELS,
    #    doc,
    #    default_model=DEFAULT_MODEL,
    #    visualizers=["parser", "ner", "tokens"],
    #    ner_labels=nlp.get_pipe("entity_ruler").labels,
    #    show_visualizer_select=True,
    #    sidebar_description=DESCRIPTION,
    #)