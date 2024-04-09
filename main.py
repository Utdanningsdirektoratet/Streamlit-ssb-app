# External libraries
import requests
import json
import pandas as pd
import csv
import io
import sys
import copy
import numpy as np
import time
import random
import re
import secrets
from pyjstat import pyjstat

# streamlit
import streamlit as st
st.set_page_config(layout="wide", page_title='ETL SSB API', page_icon = "img/favicon.ico") # page_icon = "img/api-konsoll-logo.ico"
#st.set_option('deprecation.showPyplotGlobalUse', False)
import streamlit.components.v1 as components  # Import Streamlit

# Egene Moduler
from frontend.metadata import om_statistikken
from backend.API_SSB import API_request 
from backend.payload_maker import make_payload
from backend.data_transformer import transform_12056, transform_12272, transform_12933

#### Remove red/orange header line ####
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        #MainMenu {visibility: visible;}
    </style>
'''

st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)




#### Add sidebar ####
st.sidebar.markdown("# Enkel brukerveiledning")
st.sidebar.markdown("Denne web-appen tilbyr en rekke tester som tester ut forskjellige sider av det åpne API-et")

st.sidebar.markdown(f"""
1. Tabell nummer: Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold
2. Tabell navn: Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold
3. Om statistikken: Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold
""")

st.sidebar.markdown("**Buffer (cache):**")
st.sidebar.markdown("""Denne web appen benytter en server-side buffer (cache) som lagrer responsen fra kall mot APIet. \
    Bufferen kan lagre responsen fra opp til 20 kall i opp til én time.""")

st.sidebar.markdown("""Hvis du ønsker å tømme bufferen, kan du enten trykk på knappen nedenfor eller gå inn på "hamburgermenyen" øverst \
    til høyre og trykke på "clear cache".""")
if st.sidebar.button("Tøm bufferen", type="primary"):
    st.experimental_memo.clear()
    st.runtime.legacy_caching.clear_cache()



#### Header ####
st.image("img/android-chrome-192x192.png", width=120)
st.title("ETL-redskaper for SSB statistikker (v1.0)")
st.write("Denne ETL (Extract, Transform, Load) applikasjonen henter inn, transformerer og laster ned data fra SSBs API.\
    Du velger statistikk og årgang og får ut en csv-fil som er kompatibel med USS (Utdanningsdirektoratets statistikksystem).")
st.markdown("""<p style="background-color: #708090
; color: #FFFFFF; padding: 20px"> Denne web appen benytter en server-side buffer (cache) som lagrer kall mot APIene. \
    Bufferen lagrer i utgangspunktet kun resultater av kall innen samme økt (session). Du avslutter en økt når du laster inn websiden \
        på nytt eller legger ned fanen. Hvis du ønsker at kallene skal være lagret mellom økter og for alle brukere,  trykk på radioknappen \
            nedenfor som er markert 'Global' </p>""", unsafe_allow_html=True)  # alt color #708090 color: #FFFFFF
st.markdown("***")




#### 1. Valg av statistikk ####
st.markdown("""<h2 style="color: #000000; padding: 15px;">1. Valg av statistikk </h2>"""\
    , unsafe_allow_html=True)
st.markdown("""<p style="background-color: #708090; padding: 15px;"></p>""", unsafe_allow_html=True) ##708090
st.markdown("""Denne web appen tilbyr tilgang til forskjellige SSB-statistikker gjennom deres API-løsning \
    For mer informasjon om SSBs API-løsning følg denne [lenken](https://www.ssb.no/api). """)

col1, col2 = st.columns([2, 1])

with col1:
    option_1_1 = st.selectbox('**Velg blant SSBs statistikker:**',
    ('Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold', 'Minoritetsspråklige barn i barnehager 1-5 år', 
     'Undervisningsstillinger i videregående opplæring, etter kjønn, aldersgruppe og kompetanse', 'Økonomi og undervisningspersonell VGO'), 
     help="Velg statistikk")

with col2:
    option_1_2 = st.selectbox('**Velg årgang:**', om_statistikken[option_1_1]['årgang'], help="Velg statistikk")


col3, col4 = st.columns([2, 1])

with col3:
    st.markdown("""<h4> Du har valgt: </h4>""", unsafe_allow_html=True)
    st.markdown(f"""
    * **Tabell nummer:** {om_statistikken[option_1_1]["tabell"]}
    * **Tabell navn:** {om_statistikken[option_1_1]["navn"]}
    * **Årgang:** {str(option_1_2)}
    * **Om statistikken:** {om_statistikken[option_1_1]["info"]}
    """)

    
    if st.button("Kjør spørring", type="primary") or 'button_1_1' in st.session_state:
        
        year  = option_1_2
        table = om_statistikken[option_1_1]['tabell']
        selected_payload = make_payload(table, year)
        selected_url = om_statistikken[option_1_1]['url']
        df_description, df_id, response_status, size_of = API_request(selected_url, selected_payload)

        if 'button_1_1' not in st.session_state:
            st.session_state['button_1_1'] = True

with col4:
    if 'button_1_1' in st.session_state:
        st.markdown("""<h4>Resultat av spørringen: </h4>""", unsafe_allow_html=True)
        st.markdown(f"""
        * **Url:**  {selected_url}
        * **Respons status:**  {response_status}
        * **Mottatt:**  {size_of} bytes
        """)

        st.markdown("**Json payload:**")
        st.json(selected_payload, expanded=False)

st.markdown("***")



#### 2. Rådata fra SSB ####
st.markdown("""<h2 style="color: #000000; padding: 15px;">2. Rådata fra SSB</h2>"""\
    , unsafe_allow_html=True)
st.markdown("""<p style="background-color: #708090; padding: 15px;"></p>""", unsafe_allow_html=True)


st.markdown("""Denne web appen tilbyr tilgang til forskjellige SSB statistikker gjennom deres API løsning (for mer informasjon om SSBs API løsning følg denne [lenken](https://www.ssb.no/api)). \
    I de fleste ... ...""")
mode2 = st.radio("**Velg dataformat:**", options=('Beskrivelse', 'Kode'))


if 'button_1_1' in st.session_state:
    if mode2 == 'Beskrivelse': 
        st.dataframe(df_description)
    if mode2 == 'Kode':
        st.dataframe(df_id)

st.markdown("***")



#### Transformerte data ####
st.markdown("""<h2 style="color: #000000; padding: 15px;">3. Transformerte data</h2>"""\
    , unsafe_allow_html=True)
st.markdown("""<p style="background-color: #708090; padding: 15px;"></p>""", unsafe_allow_html=True)

st.markdown("""Denne web appen tilbyr tilgang til forskjellige SSB statistikker gjennom deres API løsning (for mer informasjon om SSBs API løsning følg denne [lenken](https://www.ssb.no/api)). \
    I de fleste """)

if option_1_1 == "Barn i barnehager, etter alder, oppholdstid per uke og barnehagens eierforhold" and 'button_1_1' in st.session_state:
    df = transform_12056(df_description, df_id)
if option_1_1 == "Minoritetsspråklige barn i barnehager 1-5 år" and 'button_1_1' in st.session_state:
    df = transform_12272(df_description, df_id)
if option_1_1 == "Undervisningsstillinger i videregående opplæring, etter kjønn, aldersgruppe og kompetanse" and 'button_1_1' in st.session_state:
    df = transform_12933(df_description, df_id)


#data = pd.read_csv("data/data.csv")
if 'button_1_1' in st.session_state:
    st.dataframe(df)
    csv_file = df.to_csv(index=False, sep=";").encode('utf-8')
    st.download_button(label=":black[**Last ned data**]", data=csv_file, file_name="ssb_data.csv", mime='text/csv')
    

