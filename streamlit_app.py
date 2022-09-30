import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

posts_ref = db.collection("flights")

st.write({doc.id: doc.to_dict() for doc in posts_ref.stream()})