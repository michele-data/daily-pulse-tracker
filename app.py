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

st.divider()

st.subheader("📊 Andamento nel tempo")

if len(df) > 0:
    df["data"] = pd.to_datetime(df["data"])
    st.line_chart(df.set_index("data")[["energia", "umore", "produttivita"]])

    if show_data:
        st.dataframe(df.tail(10))
else:
    st.info("Nessun dato ancora disponibile.")

# 🧾 ANALISI NOTE
st.subheader("🧾 Analisi delle note")

if len(df) > 0 and "note" in df.columns:

    df["note"] = df["note"].fillna("")

    keyword = st.text_input("Cerca nelle note (es: lavoro, studio, stress)")

    if keyword:
        filtered = df[df["note"].str.contains(keyword, case=False, na=False)]
        st.write(f"📌 Risultati per: **{keyword}**")
        st.dataframe(filtered[["data", "energia", "umore", "produttivita", "note"]])
    else:
        st.info("Inserisci una parola per filtrare le note.")

    all_words = " ".join(df["note"].dropna()).lower().split()

    if len(all_words) > 0:
        word_series = pd.Series(all_words)
        top_words = word_series.value_counts().head(10)

        st.subheader("🔥 Parole più frequenti nelle note")
        st.dataframe(top_words)
else:
    st.info("Nessuna nota disponibile.")
