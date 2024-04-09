from backend.payload import payload_dict
import streamlit as st
import json

def make_payload(table, year):
    payload = payload_dict[table]
    payload_as_text = json.dumps(payload)
    payload = json.loads(payload_as_text.replace("YEAR", str(year)))
    return payload
