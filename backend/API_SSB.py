import requests
import streamlit as st
from pyjstat import pyjstat
import sys


@st.cache_data(ttl=3600, max_entries=20)
def API_request(url, payload):
    response = requests.post(url, json = payload)
    dataset = pyjstat.Dataset.read(response.text)
    df_description = dataset.write('dataframe')
    df_id = dataset.write('dataframe', naming='id')
    return df_description, df_id, response.status_code, sys.getsizeof(response.content)