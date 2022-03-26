import streamlit as st
import pandas as pd
import numpy as np
import srsly
import importlib
import random
from spacy.pipeline import EntityRuler # Import the Entity Ruler for making custom entities
# from st_aggrid import AgGrid

import streamlit.components.v1 as componentss

from streamlit_ace import st_ace
MODELS = srsly.read_json(Path(__file__).parent / "models.json")
DEFAULT_MODEL = "en_core_web_sm"
DEFAULT_TEXT =  "Frances Naomi Clark was an American ichthyologist born in 1894, and was one of the first woman fishery researchers to receive world-wide recognition. She attended Stanford University, and worked for the California Division of Fish and Game. Seven Ampelis cedrorum specimens were collected in a meadow near lowland fruit trees."
DESCRIPTION = """**Explore trained [spaCy v3.0](https://nightly.spacy.io) pipelines with the Proceedings of the Academy of Natural Sciences of Philadelphia (ANSP)**"""
FOOTER = """<span style="font-size: 0.75em">&hearts; Built with [`spacy-streamlit`](https://github.com/explosion/spacy-streamlit)</span>"""

title='ANSP Proceedings Explorer'
st.set_page_config(
   page_title = title,
   layout="wide",
   initial_sidebar_state="collapsed"
)

html_string = """
    <style> 
        body: { margin:0px; background-color: #FFEEEE } 
        .main .block-container { padding-top: 0px }
    </style>
    """
st.markdown(html_string, unsafe_allow_html=True)

st.markdown(":zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: :mushroom: :blowfish: :honeybee: :turtle: :fish: :octopus: :zap: ")
            
st.markdown("---")

head1, head2 = st.columns([1,2])
with head1:
	st.title(title)

sts = st.sidebar
col1, col2, col3 = st.columns([1,2,2])

volume_selection = sts.selectbox('Volume',
[
'v.44 (1892)',

'v.1 (1841-1843)',
'v.2 (1844-1845)',
'v.3 (1846-1847)',
'v.4 (1848-1849)',
'v.5 (1850-1851)',
'v.6 (1852-1853)',
'v.7 (1854-1855)',
'v.8 (1856)',
'v.9 (1857)',
'v.10 (1858)',
'v.11 (1859)',
'v.12 (1860)',
'v.13 (1861)',
'v.14 (1862)',
'v.15 (1863)',
'v.16 (1864)',
'v.17 (1865)',
'v.18 (1866)',
'v.19 (1867)',
'v.20 (1868)',
'v.21 (1869)',
'v.22 (1870)',
'v.23 (1871)',
'v.24 (1872)',
'v.25 (1873)',
'v.26 (1874)',
'v.27 (1875)',
'v.28 (1876)',
'v.29 (1877)',
'v.30 (1878)',
'v.31 (1879)',
'v.32 (1880)',
'v.33 (1881)',
'v.34 (1882)',
'v.35 (1883)',
'v.36 (1884)',
'v.37 (1885)',
'v.38 (1886)',
'v.39 (1887)',
'v.40 (1888)',
'v.41 (1889)',
'v.42 (1890)',
'v.43 (1891)',
'v.44 (1892)',
'v.45 (1893)',
'v.46 (1894)',
'v.47 (1895)',
'v.48 (1896)',
'v.49 (1897)',
'v.50 (1898)',
'v.51 (1899)',
'v.52 (1900)',
'v.53 (1901)',
'v.54 (1902)',
'v.55 (1903)',
'v.56 (1904)',
'v.57 (1905)',
'v.58 (1906)',
'v.59 (1907)',
'v.60 (1908)',
'v.61 (1909)',
'v.62 (1910)',
'v.63 (1911)',
'v.64 (1912)',
'v.65 (1913)',
'v.66 (1914)',
'v.67 (1915)',
'v.68 (1916)',
'v.69 (1917)',
'v.70 (1918)',
'v.71 (1919)',
'v.71 (1919)',
'v.72 (1920)',
'v.73 (1921)',
'v.74 (1922)',
'Proceedings, 100th Anniversary Centenary Meeting',
'Index 1812-1912 (1913)',
'v.1-62'
])

BHL_ANSP_INDEX_URL = 'https://www.biodiversitylibrary.org/item/17672#page/7/mode/1up'

if volume_selection == 'Index 1812-1912 (1913)':
    IMAGE_URL = 'https://ia600204.us.archive.org/BookReader/BookReaderImages.php?id=proceedingsofaca44acad&itemPath=%2F7%2Fitems%2Fproceedingsofaca44acad&server=ia600204.us.archive.org&page=n6_w355'
elif volume_selection == 'v.44 (1892)':
    IMAGE_URL = 'https://ia600900.us.archive.org/BookReader/BookReaderImages.php?id=proceedingsofaca44acaduoft&itemPath=%2F14%2Fitems%2Fproceedingsofaca44acaduoft&server=ia600900.us.archive.org&page=n6_w456'
else:
    IMAGE_URL = 'https://ia600306.us.archive.org/BookReader/BookReaderImages.php?id=proceedingsofaca01acad&itemPath=%2F30%2Fitems%2Fproceedingsofaca01acad&server=ia600306.us.archive.org&page=n6_w467'

DATE_COLUMN = 'date/time'
DATA_URL = ('https://fauna.ansp.org/'
            'LEADING/2021/Corpus/ANSP/workspace/app/data.csv')

with sts.expander("Sections"):
    articles=[
        'THE BIRDS OF SOUTHEASTERN TEXAS AND SOUTHERN ARIZONA OBSERVED DURING MAY, JUNE AND JULY, 1891.',
        'Article 1',
        'Article 2'
    ]
    article = st.selectbox('Article Titles',articles)

    searchTerm = st.text_input('Search Term')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = sts.text('Loading data...')
data = load_data(10000)
data_load_state.text("Data loading Done! (using st.cache)")

html_string = '<h3><a href="'+BHL_ANSP_INDEX_URL+'">BHL ANSP Index</a></h3>'
sts.markdown(html_string, unsafe_allow_html=True)

with head2:
    #my_dict = {'name': 'John', 1: [2, 4, 3]}
    #st.write(my_dict)
    st.text(volume_selection)
    st.text(article)

with col1:
    showTaxa=False
    showHabitat=False
    showLoc=False
    showPersons=False
    showDates=False
    showWorkOfArt=False

    if sts.checkbox('Persons'):
        showPersons = True
        st.subheader('Persons')
        st.write(data[data["pos"].isin(["PERSON","ORG"])])

    if sts.checkbox('Dates and Times'):
        showDates = True
        st.subheader('Dates and Times')
        st.write(data[data["pos"].isin(["DATE","TIME"])])

    if sts.checkbox('Taxa'):
        showTaxa = True
        st.subheader('Taxa')
        st.write(data[data["pos"].isin(["TAXA"])])

    if sts.checkbox('Habitat'):
        showHabitat = True
        st.subheader('Habitat')
        st.write(data[data["pos"].isin(["HABITAT"])])
    
    if sts.checkbox('Locations'):
        showLoc = True
        st.subheader('Locations')
        st.write(data[data["pos"].isin(["GPE","LOC","FAC","NORP"])])

    if sts.checkbox('Works'):
        showWorkOfArt = True
        st.subheader('Works')
        st.write(data[data["pos"].isin(["WORK_OF_ART","PRODUCT"])])
    
    if showTaxa or showHabitat or showLoc or showPersons or showDates or showWorkOfArt:
        st.text("---")
    else:
        #st.write(data)
        st.markdown("""
            <style>
            table td:nth-child(1) {
                display: none
            }
            table th:nth-child(1) {
                display: none
            }
            </style>
        """, unsafe_allow_html=True)
        st.table(data)

        #st.dataframe(data.assign(hack='').set_index('hack'))

with col2:
#    HtmlFile = open("sent.html", 'r', encoding='utf-8')
#    html_code = HtmlFile.read() 
#    #print(source_code)
#    components.html(html_code, height = 1000)

    firstLine = st.slider('Line #', 1, 100) - 1
    lastLine = firstLine + st.select_slider('# Lines', range(5,50,5))

    sentFile = open("44pg098_spacy-sents.txt", 'r', encoding='utf-8')
    sentences = sentFile.readlines()

    if searchTerm!='':
        # Spawn a new Ace editor
        content = st_ace(value=''.join(list(filter(lambda sent: sent.find(searchTerm) >= 0,sentences))[firstLine:lastLine]),wrap=True)
        line = list(filter(lambda sent: sent.find(searchTerm) >= 0,sentences))[firstLine]
    else:
        # Spawn a new Ace editor
        content = st_ace(value=''.join(sentences[firstLine:lastLine]),wrap=True)
        line = sentences[firstLine]

    import spacy
    from spacy import displacy

    st.text(line)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(line)

    import colorsys
    N = 12
    HSV_tuples = [(x*1.0/N, 0.75, 0.95) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    xRGB=[]
    for (r,g,b) in list(RGB_tuples):
        r = int(r*255)
        g = int(g*255)
        b = int(b*255)
        xRGB.append(f"#{r:X}{g:X}{b:X}")
    #st.write(xRGB)

    colors = {
        #"LOC": "linear-gradient(0deg, #aa9cfc, #fc9ce7)",
        "LOC":xRGB[0],
        "PERSON": xRGB[0],
        "ORG": xRGB[1],
        "DATE": xRGB[2],
        "TIME": xRGB[3],
        "TAXA": xRGB[4],
        "HABITAT": xRGB[5],
        "GPE": xRGB[6],
        "LOC": xRGB[7],
        "FAC": xRGB[8],
        "NORP": xRGB[9],
        "WORK_OF_ART": xRGB[10],
        "PRODUCT": xRGB[11]
    }
    ents = colors.keys()
    options = {"ents": ents, "colors": colors}
    components.html(displacy.render(doc, style="ent",options=options),height=200)

    components.html('<div style="scale:0.25;overflow:visible">'
        +displacy.render(doc, style="dep",options={"compact":True,"bg":"#EEEEEE"})
        +'</div>',
        width=600, height=400, 
        scrolling=True)
    

with col3:

    if 'key' not in st.session_state:
        st.session_state['key'] = 1

    # Reads
    #st.write(st.session_state.key)
    page = st.slider('Page #', 1, 100)

    # Updates
    st.session_state.key = page     # Attribute API
    #st.session_state['key'] = page  # Dictionary like API

    IMAGE_PAGE_OFFSET=98
    IMAGE_URL = 'https://ia600900.us.archive.org/BookReader/BookReaderImages.php?id=proceedingsofaca44acaduoft&itemPath=%2F14%2Fitems%2Fproceedingsofaca44acaduoft&server=ia600900.us.archive.org&page=n'+str(page+IMAGE_PAGE_OFFSET)+'_w456'

    #st.write(IMAGE_URL)
    st.image(IMAGE_URL)

html_string = "<h3>Link example <a href='apx/link.html'>Link</a></h3>"
sts.markdown(html_string, unsafe_allow_html=True)

with st.expander("Details",expanded=False):
    st.text(st.__path__)

