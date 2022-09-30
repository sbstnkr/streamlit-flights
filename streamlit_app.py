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

def get_chart(data):
    hover = alt.selection_single(
        fields=["date"],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    lines = (
        alt.Chart(data, title="Flights")
        .mark_line()
        .encode(
            x="date",
            y="price",
            color="city",
        )
    )

    # Draw points on the line, and highlight based on selection
    points = lines.transform_filter(hover).mark_circle(size=65)

    # Draw a rule at the location of the selection
    tooltips = (
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="date",
            y="price",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("date", title="Date"),
                alt.Tooltip("city", title="City"),
                alt.Tooltip("price", title="Price (PLN)"),
            ],
        )
        .add_selection(hover)
    )
    return (lines + points + tooltips).interactive()


chart = get_chart(df)

st.altair_chart(chart, use_container_width=True)

#st.line_chart(data=df, x='date', y='price')