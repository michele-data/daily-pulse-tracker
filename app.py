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
st.sidebar.write("App per tracciare il tuo stato giornaliero")
show_data = st.sidebar.checkbox("Mostra dati grezzi")

FILE = "data.csv"

# 📊 CARICAMENTO DATI
def carica_dati():
    try:
        if os.path.exists(FILE):
            df = pd.read_csv(FILE)

            if df is None or df.empty:
                return pd.DataFrame(columns=["data", "energia", "umore", "produttivita", "note"])

            return df
        else:
            return pd.DataFrame(columns=["data", "energia", "umore", "produttivita", "note"])

    except Exception:
        return pd.DataFrame(columns=["data", "energia", "umore", "produttivita", "note"])


# 💾 SALVATAGGIO
def salva_dati(energia, umore, produttivita, note):
    nuovo_record = pd.DataFrame([{
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "energia": energia,
        "umore": umore,
        "produttivita": produttivita,
        "note": note
    }])

    if os.path.exists(FILE):
        df_old = pd.read_csv(FILE)
        df = pd.concat([df_old, nuovo_record], ignore_index=True)
    else:
        df = nuovo_record

    df.to_csv(FILE, index=False)
    return df


df = carica_dati()

# 📥 INPUT UTENTE
energia = st.slider("Energia", 1, 10, 5)
umore = st.slider("Umore", 1, 10, 5)
produttivita = st.slider("Produttività", 1, 10, 5)
note = st.text_input("Nota (opzionale)")

if st.button("Salva giornata"):
    df = salva_dati(energia, umore, produttivita, note)
    st.success("Dati salvati con successo!")
    st.dataframe(df.tail())

st.divider()

# 📈 ANDAMENTO
st.subheader("📊 Andamento nel tempo")

if len(df) > 0:
    df["data"] = pd.to_datetime(df["data"])
    st.line_chart(df.set_index("data")[["energia", "umore", "produttivita"]])

    st.subheader("📅 Ultimi dati inseriti")

    if show_data:
        st.dataframe(df.tail(10))
else:
    st.info("Nessun dato ancora disponibile.")

st.divider()

# 🧠 INSIGHT
st.subheader("🧠 Insight automatici")

if len(df) > 3:
    media_energia = df["energia"].mean()
    media_umore = df["umore"].mean()
    media_prod = df["produttivita"].mean()

    st.write(f"📌 Energia media: **{media_energia:.2f}**")
    st.write(f"📌 Umore medio: **{media_umore:.2f}**")
    st.write(f"📌 Produttività media: **{media_prod:.2f}**")

    corr = df["energia"].corr(df["produttivita"])

    st.write("📈 Correlazione energia ↔ produttività:")

    if corr > 0.5:
        st.success(f"Relazione forte positiva ({corr:.2f})")
    elif corr > 0.2:
        st.info(f"Relazione debole positiva ({corr:.2f})")
    elif corr < -0.2:
        st.warning(f"Relazione negativa ({corr:.2f})")
    else:
        st.write(f"Nessuna relazione chiara ({corr:.2f})")
else:
    st.info("Servono almeno 4 giorni di dati.")

st.divider()

# 📅 ANALISI SETTIMANALE
st.subheader("📅 Analisi settimanale")

if len(df) > 7:
    df_week = df.copy()
    df_week["data"] = pd.to_datetime(df_week["data"])
    df_week["settimana"] = df_week["data"].dt.isocalendar().week

    settimana_corrente = df_week["settimana"].max()
    settimana_precedente = settimana_corrente - 1

    corrente = df_week[df_week["settimana"] == settimana_corrente]
    precedente = df_week[df_week["settimana"] == settimana_precedente]

    if len(precedente) > 0:
        media_corrente = corrente[["energia", "umore", "produttivita"]].mean()
        media_precedente = precedente[["energia", "umore", "produttivita"]].mean()

        diff = media_corrente - media_precedente

        st.write("📊 Confronto con settimana precedente:")

        for col in diff.index:
            val = diff[col]

            if val > 0:
                st.success(f"{col}: +{val:.2f}")
            else:
                st.warning(f"{col}: {val:.2f}")
    else:
        st.info("Serve anche la settimana precedente.")
else:
    st.info("Servono almeno 8 giorni di dati.")
