import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

flights = [{'date': doc.id,
            'data': doc.to_dict()} for doc in db.collection("flights").stream()]

print(pd.DataFrame.from_records(flights))

st.line_chart(data=flights)