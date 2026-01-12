import streamlit as st
import pandas as pd

# Konfiguration der Seite
st.set_page_config(page_title="Finanze Familiari v2", page_icon="🇨🇭", layout="centered")

# Titel
st.title("🇨🇭 Gestione Finanze: Stefano & Stephanie")
st.markdown("---")

# -----------------------------------------------------------------------------
# EINGABE-SEKTION (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.header("1. Dati Mensili (Buste Paga)")

# Stefano
st.sidebar.subheader("Stefano")
lohn_stefano = st.sidebar.number_input("Salario Versato (Netto)", value=8500.0, step=50.0, key="lohn_stefano_input")
zulagen_stefano = st.sidebar.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="zulagen_stefano_input")

# Stephanie
st.sidebar.subheader("Stephanie")
lohn_stephanie = st.sidebar.number_input("Salario Versato (Netto)", value=5000.0, step=50.0, key="lohn_stephanie_input", help="Cifra arrivata in banca")
zulagen_stephanie = st.sidebar.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="zulagen_stephanie_input")

st.sidebar.markdown("---")

# Gesundheitskosten - NEU: Aufteilung in Prämien und Rechnungen
st.sidebar.header("2. Dettaglio Salute (Busta Stephanie)")
st.sidebar.info("Inserire i costi dedotti dalla busta paga.")

# Input separati per Premi e Fatture
premi_kk_total = st.sidebar.number_input("Premi Cassa Malati (Totale)", value=1200.0, step=10.0, key="premi_kk_total")
fatture_kk_total = st.sidebar.number_input("Fatture Mediche (Totale)", value=300.0, step=10.0, key="fatture_kk_total")

# Berechnung des totalen Abzugs
total_abzug_kk = premi_kk_total + fatture_kk_total
st.sidebar.markdown(f"**Totale Dedotto:** CHF {total_abzug_kk:,.2f}")

st.sidebar.markdown("---")
st.sidebar.markdown("**Ripartizione Costi Totali (Chi ha generato la spesa?)**")
# Qui definiamo di chi sono questi costi totali (Premi + Fatture)
anteil_stefano_kk = st.sidebar.number_input("Quota Stefano (Premi + Fatture)", value=500.0, step=10.0, key="stefano_kk")
anteil_kinder_kk = st.sidebar.number_input("Quota Figlie (Premi + Fatture)", value=500.0, step=10.0, key="kinder_kk")

# Validierung
anteil_stephanie_kk = total_abzug_kk - anteil_stefano_kk - anteil_kinder_kk
if anteil_stephanie_kk < -0.01: # Kleine Toleranz für Float-Rundungen
    st.sidebar.error(f"Errore! La somma delle quote supera il totale ({total_abzug_kk}).")
else:
    st.sidebar.caption(f"Quota residua Stephanie: CHF {anteil_stephanie_kk:.2f}")

st.sidebar.markdown("---")

# Budget Ziel
st.sidebar.header("3. Budget Comune")
budget_ziel = st.sidebar.number_input("Obiettivo Conto Comune", value=7000.0, step=100.0, key="budget_ziel")

# -----------------------------------------------------------------------------
# BERECHNUNGS-LOGIK
# -----------------------------------------------------------------------------

# 1. Rekonstruktion des bereinigten Nettoeinkommens
basis_stefano = lohn_stefano - zulagen_stefano
basis_stephanie = (lohn_stephanie - zulagen_stephanie) + total_abzug_kk
total_basis = basis_stefano + basis_stephanie

# 2. Berechnung des Verteilschlüssels (Ratios)
if total_basis > 0:
    quote_stefano = basis_stefano / total_basis
    quote_stephanie = basis_stephanie / total_basis
else:
    quote_stefano = 0.5
