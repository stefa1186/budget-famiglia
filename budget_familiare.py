import streamlit as st
import pandas as pd

# Konfiguration der Seite
st.set_page_config(page_title="Gestione Finanze Familiari", page_icon="🇨🇭", layout="centered")

# Titel und Einleitung
st.title("🇨🇭 Gestione Finanze: Stefano & Stephanie")
st.markdown("---")

# -----------------------------------------------------------------------------
# EINGABE-SEKTION (SIDEBAR)
# -----------------------------------------------------------------------------
st.sidebar.header("1. Dati Mensili (Buste Paga)")

# Daten Stefano
st.sidebar.subheader("Stefano")
# WICHTIG: Wir nutzen 'key', um die Felder eindeutig zu identifizieren
lohn_stefano = st.sidebar.number_input("Salario Versato (Netto)", min_value=0.0, value=8500.0, step=50.0, key="lohn_stefano_input", help="Cifra arrivata in banca")
zulagen_stefano = st.sidebar.number_input("di cui Assegni Familiari", min_value=0.0, value=250.0, step=50.0, key="zulagen_stefano_input")

# Daten Stephanie
st.sidebar.subheader("Stephanie")
# Auch hier 'key' hinzufügen, sonst gibt es einen DuplicateElementId Fehler
lohn_stephanie = st.sidebar.number_input("Salario Versato (Netto)", min_value=0.0, value=5000.0, step=50.0, key="lohn_stephanie_input", help="Cifra arrivata in banca")
zulagen_stephanie = st.sidebar.number_input("di cui Assegni Familiari", min_value=0.0, value=250.0, step=50.0, key="zulagen_stephanie_input")

st.sidebar.markdown("---")

# Gesundheitskosten
st.sidebar.header("2. Dettaglio Salute (Busta Stephanie)")
st.sidebar.info("Inserire i dati dedotti dalla busta paga di Stephanie.")

total_abzug_kk = st.sidebar.number_input("Totale Dedotto (Cassa Malati + Fatture)", min_value=0.0, value=1500.0, step=10.0, key="total_kk")
anteil_stefano_kk = st.sidebar.number_input("Quota Stefano", min_value=0.0, value=500.0, step=10.0, key="stefano_kk")
anteil_kinder_kk = st.sidebar.number_input("Quota Figlie (Frida & Alma)", min_value=0.0, value=500.0, step=10.0, key="kinder_kk")

# Validierung
anteil_stephanie_kk = total_abzug_kk - anteil_stefano_kk - anteil_kinder_kk
if anteil_stephanie_kk < 0:
    st.sidebar.error("Attenzione! La somma delle quote supera il totale dedotto.")

st.sidebar.markdown(f"**Quota calcolata Stephanie:** CHF {anteil_stephanie_kk:.2f}")

st.sidebar.markdown("---")

# Budget Ziel
st.sidebar.header("3. Budget Comune")
budget_ziel = st.sidebar.number_input("Obiettivo Conto Comune", min_value=0.0, value=7000.0, step=100.0, key="budget_ziel", help="Affitto, Spesa, Nido, Svago")

# -----------------------------------------------------------------------------
# BERECHNUNGS-LOGIK (CORE)
# -----------------------------------------------------------------------------

# 1. Rekonstruktion des bereinigten Nettoeinkommens
basis_stefano = lohn_stefano - zulagen_stefano
basis_stephanie = (lohn_stephanie - zulagen_stephanie) + total_abzug_kk
total_basis = basis_stefano + basis_stephanie

# 2. Berechnung des Verteilschlüssels
if total_basis > 0:
    quote_stefano = basis_stef
