# A Streamlit app to show text from the Proceedings of the Academy of Natural Sciences of Philadelphia annotated with custom NER entities for taxonomic names and habitats. 

This app is not so far off from the default [spaCy Streamlit app](https://share.streamlit.io/ines/spacy-streamlit-demo/master/app.py), but it adds:
1. an option to upload a text file for NLP
2. Custom entity ruler pipes to tag:
  * taxonomic names (prepared in [previous efforts](https://amandawhitmire.github.io/blog/posts/2021-09-16-scrape-all-taxa/)) and
  * habitat terms (from: Nguyen N, Gabud R, Ananiadou S (2019) COPIOUS: A gold standard corpus of named entities towards extracting species occurrence from biodiversity literature. Biodiversity Data Journal 7: e29626. https://doi.org/10.3897/BDJ.7.e29626)

I will continue to develop the look and feel of this app, and improve functionality around longer texts (e.g. full ANSP articles) with caching. I'd also like to use the [Annotated Text Component for Streamlit](https://github.com/tvst/st-annotated-text) to visualize the tokens. 
