import spacy_streamlit
import streamlit as st
import spacy
import pandas as pd
from pathlib import Path
import srsly
import importlib
import random
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities
from st_aggrid import AgGrid

st.set_page_config(layout="wide")

MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. She attended Stanford University, and worked for the California Division of Fish and Game. Seven Ampelis cedrorum specimens were collected in a meadow near lowland fruit trees."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia (ANSP)**"""
FOOTER = """<span style="font-size: 0.75em">&hearts; Built with [`spacy-streamlit`](https://github.com/explosion/spacy-streamlit)</span>"""

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# NOTE: custom patterns have already been created for the NLP Pipeline > Entity Ruler via the ruler.py file.

st.title("Custom NER pipeline for taxonomic names & habitats")

st.markdown("I am currently working on a project to explore the corpus of the *Proceedings of the Academy of Natural Sciences of Philadelphia* (1841 - 1922), available at the [Biodiversity Heritage Library](https://www.biodiversitylibrary.org/bibliography/6885). I am interested in how this corpus may be leveraged for historical species occurrence data. Species names in the text have already been identified via the [Global Names Finder](https://doi.org/10.5281/zenodo.5111562), but which of these could be an occurrence record ('I saw this thing, at this place, at this time.')? I'm hoping to leverge the power of NLP with spaCy, and this app serves as a demo of what we can accomplish.")

st.markdown(":zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: ")
            
st.markdown("---")

# SIDEBAR START ---------------------------- 
with st.sidebar:
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        st.write("")

    with col2:
        st.image('https://raw.githubusercontent.com/amandawhitmire/streamlit-ansp/master/images/leading-logo-1.png')

    with col3:
        st.write("")
    
    st.write(DESCRIPTION)    
    st.write("") # vertical spacing
    st.markdown("## How does it work?")
    st.markdown("Upload a text file or paste text into the box to explore named entities and the results of spaCy's natural language processing pipeline. Keep in mind that the set of habitat entities are from [Nguyen et al. 2019](https://doi.org/10.3897/BDJ.7.e29626) & the taxonomic names were mined from the ANSP corpus using Global Names [GNfinder](https://github.com/gnames/gnfinder). If you upload non-ANSP text, some taxonomic names will get missed.  Download the CSV table to continue your work outside of this app.")
    st.markdown("**NOTE**: The set of taxonomic names includes over 160,000 items - please be patient as the app runs, and be mindful of the length of your text file. I will work to speed it up!")
    st.write("") # vertical spacing
    st.markdown(":owl: **Future Work**  :owl: ")
    st.write("Future versions of this app will supply you with sample ANSP texts to look at. We are working on curating interesting subsets of the corpus.")
    

    #st.write("## Model")
    #model = st.selectbox(
    #    "Which model would you like to use?", ["English | Small", "English | Medium", "English | Large", "English | TRF"]
    #)
    
    #for i in range(int(st.number_input('Num:'))): foo()
    #if st.sidebar.selectbox('I:',['f']) == 'f': b()
    #my_slider_val = st.slider('Quinn Mallory', 1, 88)
    #st.write(slider_val)
    
    st.write("") # vertical padding
    st.markdown(
        FOOTER,
        unsafe_allow_html=True,
    )
# SIDEBAR END ---------------------------- 

# FILE UPLOADER ----------------------------
st.markdown(":sparkles: **Upload Text File** :sparkles: ")
uploaded_file = st.file_uploader("File Upload", type=["txt"])
# FILE UPLOADER ----------------------------

st.markdown("---")

if uploaded_file is not None:
    
    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.from_disk(Path(__file__).parent / "../data/ansp-patterns.jsonl")
    doc = nlp(uploaded_file.getvalue().decode("utf-8"))
    
    # to plot the labels for the custom etitites, we have to make a new set.
    # thank you to Jeremy Nelson for helping me figure this out. 
    labels=list(nlp.get_pipe("ner").labels)
    for label in nlp.get_pipe("entity_ruler").labels:
        labels.append(label)
        
    colors = {"CARDINAL":"#DB9D85","DATE":"#D0A374","EVENT":"#C2A968","FAC":"#B1AF64","GPE":"#9DB469","HABITAT":"#86B875","LANGUAGE":"#6DBC86","LAW":"#53BE98","LOC":"#3DBEAB","MONEY":"#39BDBC","NORP":"#4CB9CC","ORDINAL":"#69B4D8","ORG":"#87AEDF","PERCENT":"#A3A7E2","PERSON":"#BB9FE0","PRODUCT":"#CD99D8","QUANTITY":"#DA95CC","TAXA":"#E293BD","TIME":"#E494AB","WORK_OF_ART":"#E29898","HABITAT":"#86B875","TAXA":"#E293BD"}
    
    spacy_streamlit.visualize_ner(
        doc, 
        labels=labels, 
        colors=colors,
        title="Custom Entity Labels",
        show_table=False,
        # sidebar_title="sidebar title", # doesn't work
    )
    
    st.markdown('## Exploring the Tokens')
    # Create dataframe for data download
    rows = []
    for token in doc:
        rows.append(
            {
                'Token': token.text, 
                'Lemma': token.lemma_,
                'POS': token.pos_,
                'Tag': token.tag_,
                'Dependency': token.dep_,
                'Head': token.head,
                'Ent Type': token.ent_type_,
                'IsAlpha': token.is_alpha,
                'IsPunct': token.is_punct,
                'IsStop': token.is_stop
            }
        )   
    tokes = pd.DataFrame(rows)
    csv = convert_df(tokes)
    
    AgGrid(tokes)
    
    # Download the tokens?
    st.download_button(
        label="Download TOKEN DATA as CSV",
        data =csv,
        file_name='tokens.csv',
        mime='text/csv',
    )
    st.text(f"Analyzed using spaCy model {DEFAULT_MODEL}")
    
# IF NO FILE UPLOADED ---------------------
else:
    st.markdown(":sparkles: **Paste Text Here** :sparkles: ")
    text = st.text_area("(Default text is shown)",DEFAULT_TEXT, height=200)

    nlp = spacy.load(DEFAULT_MODEL)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    ruler.from_disk(Path(__file__).parent / "../data/ansp-patterns.jsonl")
    doc = nlp(text)
    
    # to plot the labels for the custom etitites, we have to make a new set.
    # thank you to Jeremy Nelson for helping me figure this out. 
    labels=list(nlp.get_pipe("ner").labels)
    for label in nlp.get_pipe("entity_ruler").labels:
        labels.append(label)
    
    colors = {"CARDINAL":"#DB9D85","DATE":"#D0A374","EVENT":"#C2A968","FAC":"#B1AF64","GPE":"#9DB469","HABITAT":"#86B875","LANGUAGE":"#6DBC86","LAW":"#53BE98","LOC":"#3DBEAB","MONEY":"#39BDBC","NORP":"#4CB9CC","ORDINAL":"#69B4D8","ORG":"#87AEDF","PERCENT":"#A3A7E2","PERSON":"#BB9FE0","PRODUCT":"#CD99D8","QUANTITY":"#DA95CC","TAXA":"#E293BD","TIME":"#E494AB","WORK_OF_ART":"#E29898","HABITAT":"#86B875","TAXA":"#E293BD"}
    
    # show the labeled text
    spacy_streamlit.visualize_ner(
        doc, 
        labels=labels, 
        colors=colors,
        title="Custom Entity Labels",
        show_table=False,
        )
    
    st.markdown('## Exploring the Tokens')
    # Create dataframe for data download
    rows = []
    for token in doc:
        rows.append(
            {
                'Token': token.text, 
                'Lemma': token.lemma_,
                'POS': token.pos_,
                'Tag': token.tag_,
                'Dependency': token.dep_,
                'Head': token.head,
                'Ent Type': token.ent_type_,
                'IsAlpha': token.is_alpha,
                'IsPunct': token.is_punct,
                'IsStop': token.is_stop
            }
        )   
    tokes = pd.DataFrame(rows)
    csv = convert_df(tokes)
    
    AgGrid(tokes)
        
    # Download the tokens?
    st.download_button(
        label="Download TOKEN DATA as CSV",
        data =csv,
        file_name='tokens.csv',
        mime='text/csv',
    )

    st.text(f"Analyzed using spaCy model {DEFAULT_MODEL}")
    
# this is the code for using the built-in tokens visualizer. 
# I do not use this because it does not use the custom entity ruler in the
# table, even though the correct pipeline results are available in the download.
# I also really like the AggGrid options to filter the data in the table.

#spacy_streamlit.visualize(
#    MODELS,
#    doc,
#    default_model=DEFAULT_MODEL,
#    visualizers=["tokens"],
#    show_visualizer_select=False,
#    sidebar_description=DESCRIPTION,
#)