import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json
import pandas as pd
import altair as alt


key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

flights = []
for doc in db.collection("flights").stream():
    flights.append({'date': doc.id,
                    'cities': doc.get('cities')})

df = pd.json_normalize(flights, record_path=['cities'], meta='date')
df = df[['date', 'city', 'price']]

print(df)

c = alt.Chart(df).mark_line().encode(
    x='date', y='price', size='city', color='city', tooltip=['price', 'city', 'date']
)

st.altair_chart(c, use_container_width=True)

#st.line_chart(data=df, x='date', y='price')