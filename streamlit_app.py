import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd


key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

flights = []
for doc in db.collection("flights").stream():
    flights.append({'date': doc.id,
                    'cities': doc.get('cities')})

df = pd.json_normalize(flights, record_path=['cities'], meta='date')

st.line_chart(data=df, x='date', y=['city', 'price'])