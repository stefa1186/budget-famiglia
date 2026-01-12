import streamlit as st
import pandas as pd

# Konfiguration der Seite
# Wir setzen das Layout auf "wide", damit wir auf dem Desktop mehr Platz haben.
st.set_page_config(page_title="Gestione Finanze Familiari", page_icon="🇨🇭", layout="centered")

# Titel und Einleitung
st.title("🇨🇭 Gestione Finanze: Stefano & Stephanie")
st.markdown("---")

# -----------------------------------------------------------------------------
# EINGABE-SEKTION (SIDEBAR)
# Hier werden die monatlichen variablen Daten erfasst.
# -----------------------------------------------------------------------------
st.sidebar.header("1. Dati Mensili (Buste Paga)")

# Daten Stefano
st.sidebar.subheader("Stefano")
lohn_stefano = st.sidebar.number_input("Salario Versato (Netto)", min_value=0.0, value=8500.0, step=50.0, help="Cifra arrivata in banca")
zulagen_stefano = st.sidebar.number_input("di cui Assegni Familiari", min_value=0.0, value=250.0, step=50.0)

# Daten Stephanie
st.sidebar.subheader("Stephanie")
lohn_stephanie = st.sidebar.number_input("Salario Versato (Netto)", min_value=0.0, value=5000.0, step=50.0, help="Cifra arrivata in banca")
zulagen_stephanie = st.sidebar.number_input("di cui Assegni Familiari", min_value=0.0, value=250.0, step=50.0)

st.sidebar.markdown("---")

# Gesundheitskosten (Detaillierung der Abzüge bei Stephanie)
st.sidebar.header("2. Dettaglio Salute (Busta Stephanie)")
st.sidebar.info("Inserire i dati dedotti dalla busta paga di Stephanie.")

total_abzug_kk = st.sidebar.number_input("Totale Dedotto (Cassa Malati + Fatture)", min_value=0.0, value=1500.0, step=10.0)
anteil_stefano_kk = st.sidebar.number_input("Quota Stefano", min_value=0.0, value=500.0, step=10.0)
anteil_kinder_kk = st.sidebar.number_input("Quota Figlie (Frida & Alma)", min_value=0.0, value=500.0, step=10.0)

# Validierung: Der Rest ist Stephanies Anteil
anteil_stephanie_kk = total_abzug_kk - anteil_stefano_kk - anteil_kinder_kk
if anteil_stephanie_kk < 0:
    st.sidebar.error("Attenzione! La somma delle quote supera il totale dedotto.")

st.sidebar.markdown(f"**Quota calcolata Stephanie:** CHF {anteil_stephanie_kk:.2f}")

st.sidebar.markdown("---")

# Budget Ziel
st.sidebar.header("3. Budget Comune")
budget_ziel = st.sidebar.number_input("Obiettivo Conto Comune", min_value=0.0, value=7000.0, step=100.0, help="Affitto, Spesa, Nido, Svago")

# -----------------------------------------------------------------------------
# BERECHNUNGS-LOGIK (CORE)
# Hier wird der Verteilschlüssel und die Netting-Logik angewendet.
# -----------------------------------------------------------------------------

# 1. Rekonstruktion des bereinigten Nettoeinkommens (Wirtschaftskraft)
# Wir entfernen die Zulagen und addieren bei Stephanie die Gesundheitskosten wieder hinzu.
basis_stefano = lohn_stefano - zulagen_stefano
basis_stephanie = (lohn_stephanie - zulagen_stephanie) + total_abzug_kk
total_basis = basis_stefano + basis_stephanie

# 2. Berechnung des Verteilschlüssels
if total_basis > 0:
    quote_stefano = basis_stefano / total_basis
    quote_stephanie = basis_stephanie / total_basis
else:
    quote_stefano = 0.5
    quote_stephanie = 0.5

# 3. Berechnung der Finanzierung des Gemeinschaftskontos
# Die Zulagen fliessen zu 100% ein, der Rest wird aufgeteilt.
total_zulagen = zulagen_stefano + zulagen_stephanie
restfinanzierung = budget_ziel - total_zulagen

transfer_stefano_budget = restfinanzierung * quote_stefano
transfer_stephanie_budget = restfinanzierung * quote_stephanie

# 4. Berechnung der privaten Rückerstattung (Gesundheit)
# Stefano schuldet Stephanie 100% seiner Kosten und seinen Anteil an den Kindern.
schuld_stefano_total = anteil_stefano_kk + (anteil_kinder_kk * quote_stefano)

# -----------------------------------------------------------------------------
# ANZEIGE (OUTPUT UI)
# Visualisierung der Resultate für den Benutzer.
# -----------------------------------------------------------------------------

st.header("📊 Analisi del Mese")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Reddito Reale Stefano", f"CHF {basis_stefano:,.0f}".replace(",", "'"))
    st.caption(f"Ratio: {quote_stefano*100:.1f}%")
with col2:
    st.metric("Reddito Reale Stephanie", f"CHF {basis_stephanie:,.0f}".replace(",", "'"))
    st.caption(f"Ratio: {quote_stephanie*100:.1f}%")
with col3:
    st.metric("Totale Potenza Famiglia", f"CHF {total_basis:,.0f}".replace(",", "'"))

st.divider()

st.subheader("🚀 Lista Bonifici da Eseguire")
st.markdown("Effettuate questi 5 bonifici esatti per bilanciare tutto perfettamente.")

# Wir nutzen Container für eine saubere Darstellung der 3 Kategorien.

# A. Zulagen
with st.container():
    st.markdown("#### A. Trasferimento Assegni Familiari (al Conto Comune)")
    c1, c2 = st.columns(2)
    c1.success(f"**Stefano versa:** CHF {zulagen_stefano:.2f}")
    c2.success(f"**Stephanie versa:** CHF {zulagen_stephanie:.2f}")

# B. Budget
with st.container():
    st.markdown("#### B. Contributo Spese Comuni (al Conto Comune)")
    st.caption(f"Necessari CHF {restfinanzierung:,.2f} divisi in base al reddito reale.")
    c1, c2 = st.columns(2)
    c1.info(f"**Stefano versa:** CHF {transfer_stefano_budget:,.2f}")
    c2.info(f"**Stephanie versa:** CHF {transfer_stephanie_budget:,.2f}")

# C. Rimborso Salute
with st.container():
    st.markdown("#### C. Rimborso Salute (da Stefano a Stephanie)")
    st.warning(f"**Stefano versa a Stephanie:** CHF {schuld_stefano_total:,.2f}")
    with st.expander("Dettaglio del calcolo rimborso"):
        st.write(f"- 100% Salute Stefano: CHF {anteil_stefano_kk:.2f}")
        st.write(f"- {quote_stefano*100:.1f}% Salute Figlie ({anteil_kinder_kk}): CHF {anteil_kinder_kk * quote_stefano:.2f}")
        st.write(f"**Totale:** CHF {schuld_stefano_total:.2f}")

st.divider()

# Zusammenfassungstabelle für die Archivierung
st.subheader("📝 Riepilogo per Archivio")
df_summary = pd.DataFrame({
    "Descrizione": ["Versamento Stefano (Assegni)", "Versamento Stephanie (Assegni)", 
                    "Versamento Stefano (Spese)", "Versamento Stephanie (Spese)", 
                    "Rimborso Salute (S->S)"],
    "Destinatario": ["Conto Comune", "Conto Comune", "Conto Comune", "Conto Comune", "Privato Stephanie"],
    "Importo (CHF)": [zulagen_stefano, zulagen_stephanie, transfer_stefano_budget, 
                      transfer_stephanie_budget, schuld_stefano_total]
})
st.table(df_summary.style.format({"Importo (CHF)": "{:.2f}"}))
