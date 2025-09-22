import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_dividenden():
    try:
        # === Portfolio laden ===
        uploaded_file = st.file_uploader("📂 Lade dein Portfolio hoch", type=["xlsx", "csv"])

        if uploaded_file is not None:
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
        else:
            # Fallback: versuche portfolio.csv oder portfolio.xlsx
            try:
                df = pd.read_excel("portfolio.xlsx")
                st.info("Portfolio aus portfolio.xlsx geladen ✅")
            except FileNotFoundError:
                df = pd.read_csv("portfolio.csv")
                st.info("Portfolio aus portfolio.csv geladen ✅")

    except FileNotFoundError:
        st.error("❌ portfolio.csv oder portfolio.xlsx nicht gefunden.")
        return pd.DataFrame()

    # Spalten prüfen
    if "Dividende_pro_Aktie" not in df.columns or "Shares" not in df.columns:
        st.warning("⚠️ Deine Datei benötigt mindestens die Spalten: `Shares`, `Dividende_pro_Aktie`")
        return pd.DataFrame()

    # Berechnungen
    df["Dividende_Jahr"] = df["Shares"] * df["Dividende_pro_Aktie"]
    df["Dividende_Monat"] = df["Dividende_Jahr"] / 12

    return df


# === Hauptprogramm ===
st.title("💰 Dividenden Tracker")

dividenden_df = load_dividenden()

if not dividenden_df.empty:
    st.subheader("📊 Portfolio Übersicht")
    st.dataframe(dividenden_df)

    # Diagramm erstellen
    fig, ax = plt.subplots()
    dividenden_df.groupby("Aktie")["Dividende_Jahr"].sum().plot(kind="bar", ax=ax)
    ax.set_ylabel("Dividende pro Jahr (€)")
    ax.set_title("Dividenden pro Aktie")
    st.pyplot(fig)
