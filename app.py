import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="Daily Pulse Tracker",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🧠 Daily Pulse Tracker")
st.write("Registra ogni giorno il tuo stato mentale e produttivo.")

st.sidebar.title("⚙️ Controlli")
show_data = st.sidebar.checkbox("Mostra dati grezzi")

FILE = "data.csv"


def carica_dati():
    if (not os.path.exists(FILE)) or os.path.getsize(FILE) == 0:
        return pd.DataFrame(columns=["data", "energia", "umore", "produttivita", "note"])

    try:
        return pd.read_csv(FILE)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=["data", "energia", "umore", "produttivita", "note"])


def salva_dati(energia, umore, produttivita, note):
    nuovo_record = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "energia": energia,
        "umore": umore,
        "produttivita": produttivita,
        "note": note
    }])

    df_old = carica_dati()

    df = pd.concat([df_old, nuovo_record], ignore_index=True)
    df.to_csv(FILE, index=False)

    return df


energia = st.slider("Energia", 1, 10, 5)
umore = st.slider("Umore", 1, 10, 5)
produttivita = st.slider("Produttività", 1, 10, 5)
note = st.text_input("Nota (opzionale)")

df = carica_dati()

if st.button("Salva giornata"):
    df = salva_dati(energia, umore, produttivita, note)
    st.success("Dati salvati con successo!")
    st.dataframe(df.tail())

# 🧠 INSIGHT AUTOMATICI
st.divider()
st.subheader("🧠 Insight automatici")

if len(df) > 3:

    media_energia = df["energia"].mean()
    media_umore = df["umore"].mean()
    media_prod = df["produttivita"].mean()

    st.write(f"📌 Energia media: {media_energia:.2f}")
    st.write(f"📌 Umore medio: {media_umore:.2f}")
    st.write(f"📌 Produttività media: {media_prod:.2f}")

else:
    st.info("Servono almeno 4 giorni di dati.")

st.divider()

# 🎛️ FILTRO TABELLA
st.subheader("🎛️ Filtro dati")

if len(df) > 0:

    col1, col2, col3 = st.columns(3)

    with col1:
        show_energia = st.checkbox("Energia", value=True)

    with col2:
        show_umore = st.checkbox("Umore", value=True)

    with col3:
        show_prod = st.checkbox("Produttività", value=True)

    columns_to_show = ["data"]

    if show_energia:
        columns_to_show.append("energia")
    if show_umore:
        columns_to_show.append("umore")
    if show_prod:
        columns_to_show.append("produttivita")

    st.dataframe(df[columns_to_show])
else:
    st.info("Nessun dato disponibile.")
    st.info("Nessuna nota disponibile.")
