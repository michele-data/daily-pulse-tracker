import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Daily Pulse Tracker", layout="centered")

st.title("🧠 Daily Pulse Tracker")
st.write("Registra ogni giorno il tuo stato mentale e produttivo.")

FILE = "data.csv"

# 📥 INPUT UTENTE
energia = st.slider("Energia", 1, 10, 5)
umore = st.slider("Umore", 1, 10, 5)
produttivita = st.slider("Produttività", 1, 10, 5)
note = st.text_input("Nota (opzionale)")

def salva_dati():
    nuovo_record = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "energia": energia,
        "umore": umore,
        "produttivita": produttivita,
        "note": note
    }])

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, nuovo_record], ignore_index=True)
    else:
        df = nuovo_record

    df.to_csv(FILE, index=False)
    return df

if st.button("Salva giornata"):
    df = salva_dati()
    st.success("Dati salvati con successo!")

    st.dataframe(df.tail())
