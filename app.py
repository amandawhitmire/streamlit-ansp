import spacy_streamlit
import streamlit as st
import spacy
from pathlib import Path
import srsly
import importlib
import random
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities

st.set_page_config(layout="wide")

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. She attended Stanford University, and worked for the California Division of Fish and Game. Seven Ampelis cedrorum specimens were collected in a meadow near lowland fruit trees."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia**"""

# NOTE: custom patterns have already been created for the NLP Pipeline > Entity Ruler via the ruler.py file.

st.title("Custom NER pipeline for taxonomic names & habitats")

st.markdown("I am currently working on a project to explore the corpus of the Proceedings of the Academy of Natural Sciences of Philadelphia (1841 - 1922), available at the [Biodiversity Heritage Library](https://www.biodiversitylibrary.org/bibliography/6885). I am interested in how this corpus may be leveraged for historical species occurrence data. Species names in the text have already been identified via the [Global Names Finder](https://doi.org/10.5281/zenodo.5111562), but which of these could be an occurrence record ('I saw this thing, at this place, at this time.')? I'm hoping to leverge the power of NLP with spaCy, and this app serves as a demo of what we can accomplish.")

st.markdown(":zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: ")
            
st.markdown("---")

# FILE UPLOADER
st.markdown(":sparkles: **Upload Text File** :sparkles: ")
uploaded_file = st.file_uploader("File Upload", type=["txt"])

st.markdown("---")

if uploaded_file is not None:
    
    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.from_disk(Path(__file__).parent / "ansp-patterns.jsonl")
    doc = nlp(uploaded_file.getvalue().decode("utf-8"))
    
    #for ent in doc.ents:
    #    st.write(ent.text, ",", ent.label_)
    
    labels=list(nlp.get_pipe("ner").labels)
    for label in nlp.get_pipe("entity_ruler").labels:
        labels.append(label)
        
    colors = {"CARDINAL":"#DB9D85","DATE":"#D0A374","EVENT":"#C2A968","FAC":"#B1AF64","GPE":"#9DB469","HABITAT":"#86B875","LANGUAGE":"#6DBC86","LAW":"#53BE98","LOC":"#3DBEAB","MONEY":"#39BDBC","NORP":"#4CB9CC","ORDINAL":"#69B4D8","ORG":"#87AEDF","PERCENT":"#A3A7E2","PERSON":"#BB9FE0","PRODUCT":"#CD99D8","QUANTITY":"#DA95CC","TAXA":"#E293BD","TIME":"#E494AB","WORK_OF_ART":"#E29898","HABITAT":"#86B875","TAXA":"#E293BD"}
    
    spacy_streamlit.visualize_ner(
        doc, 
        labels=labels, 
        colors=colors,
        title="Custom Entity Pipeline",
        show_table=False,
        # sidebar_title="sidebar title", # doesn't work
    )
    st.text(f"Analyzed using spaCy model {DEFAULT_MODEL}")
    
    st.markdown('## Exploring the Tokens')
    
    spacy_streamlit.visualize(
        MODELS,
        doc,
        default_model=DEFAULT_MODEL,
        visualizers=["tokens"],
        show_visualizer_select=False,
        sidebar_description=DESCRIPTION,
    )

# IF NO FILE UPLOADED
else:
    
    text = st.text_area("Text to analyze", DEFAULT_TEXT, height=200)

    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.from_disk(Path(__file__).parent / "ansp-patterns.jsonl")
    doc = nlp(text)
    
    #for ent in doc.ents:
    #    st.write(ent.text, ",", ent.label_)
    
    labels=list(nlp.get_pipe("ner").labels)
    for label in nlp.get_pipe("entity_ruler").labels:
        labels.append(label)
    
    colors = {"CARDINAL":"#DB9D85","DATE":"#D0A374","EVENT":"#C2A968","FAC":"#B1AF64","GPE":"#9DB469","HABITAT":"#86B875","LANGUAGE":"#6DBC86","LAW":"#53BE98","LOC":"#3DBEAB","MONEY":"#39BDBC","NORP":"#4CB9CC","ORDINAL":"#69B4D8","ORG":"#87AEDF","PERCENT":"#A3A7E2","PERSON":"#BB9FE0","PRODUCT":"#CD99D8","QUANTITY":"#DA95CC","TAXA":"#E293BD","TIME":"#E494AB","WORK_OF_ART":"#E29898","HABITAT":"#86B875","TAXA":"#E293BD"}
    
    # options = {"ents": labels, "colors": ner_colors}
    # st.write(labels)
    # st.write(colors)
    
    spacy_streamlit.visualize_ner(
        doc, 
        labels=labels, 
        colors=colors,
        title="Custom Entity Pipeline",
        show_table=False,
    )
    st.text(f"Analyzed using spaCy model {DEFAULT_MODEL}")
    
    st.markdown('## Exploring the Tokens')
    
    spacy_streamlit.visualize(
        MODELS,
        doc,
        default_model=DEFAULT_MODEL,
        visualizers=["tokens"],
        show_visualizer_select=False,
        sidebar_description=DESCRIPTION,
    )