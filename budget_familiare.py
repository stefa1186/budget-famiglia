import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 0. CONFIGURAZIONE PAGINA
# Impostiamo "wide" così usa tutto lo schermo (destra e sinistra)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Finanze Familiari", page_icon="🇨🇭", layout="wide")

# -----------------------------------------------------------------------------
# 1. INPUT (BARRA LATERALE - SINISTRA)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.header("1. Dati Buste Paga")
    
    st.subheader("Stefano")
    lohn_stefano = st.number_input("Salario Versato (Netto)", value=8500.0, step=50.0, key="stef_sal")
    zulagen_stefano = st.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="stef_ass")
    
    st.markdown("---")
    
    st.subheader("Stephanie")
    lohn_stephanie = st.number_input("Salario Versato (Netto)", value=5000.0, step=50.0, key="steph_sal")
    zulagen_stephanie = st.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="steph_ass")
    
    st.header("2. Dati Salute (Stephanie)")
    st.info("Inserire costi totali (Premi + Fatture)")
    
    # Input separati
    premi_kk = st.number_input("Premi Cassa Malati", value=1200.0, step=10.0, key="kk_premi")
    fatture_kk = st.number_input("Fatture Mediche", value=300.0, step=10.0, key="kk_fatt")
    total_abzug_kk = premi_kk + fatture_kk
    
    st.write(f"**Totale Dedotto:** CHF {total_abzug_kk:,.2f}")
    
    st.markdown("---")
    st.markdown("**Chi ha generato la spesa?**")
    
    anteil_stefano_kk = st.number_input("Quota Stefano", value=500.0, step=10.0, key="q_stef")
    anteil_kinder_kk = st.number_input("Quota Figlie", value=500.0, step=10.0, key="q_kind")
    
    # Calcolo residuo Stephanie
    anteil_stephanie_kk = total_abzug_kk - anteil_stefano_kk - anteil_kinder_kk
    
    if anteil_stephanie_kk < -0.1:
        st.error(f"Errore: Quote > Totale ({total_abzug_kk})")
    else:
        st.caption(f"Quota Stephanie: CHF {anteil_stephanie_kk:.2f}")

    st.header("3. Obiettivo Comune")
    budget_ziel = st.number_input("Budget Mensile Necessario", value=7000.0, step=100.0, key="bud_ziel")

# -----------------------------------------------------------------------------
# 2. LOGICA DI CALCOLO (Il motore matematico)
# -----------------------------------------------------------------------------

# Reddito Reale (Base imponibile per il calcolo ratio)
basis_stefano = lohn_stefano - zulagen_stefano
basis_stephanie = (lohn_stephanie - zulagen_stephanie) + total_abzug_kk
total_basis = basis_stefano + basis_stephanie

# Ratio (Percentuali)
if total_basis > 0:
    quote_stefano = basis_stefano / total_basis
    quote_stephanie = basis_stephanie / total_basis
else:
    quote_stefano = 0.5
    quote_stephanie = 0.5

# Soldi da versare
total_zulagen = zulagen_stefano + zulagen_stephanie
restfinanzierung = budget_ziel - total_zulagen

transfer_stefano_budget = restfinanzierung * quote_stefano
transfer_stephanie_budget = restfinanzierung * quote_stephanie

# Debito Salute
schuld_stefano_total = anteil_stefano_kk + (anteil_kinder_kk * quote_stefano)

# -----------------------------------------------------------------------------
# 3. OUTPUT (PARTE CENTRALE/DESTRA)
# -----------------------------------------------------------------------------

# Titolo Principale
st.title("🇨🇭 Gestione Finanze: Stefano & Stephanie")
st.markdown("---")

# Sezione A: Analisi Reddito (in alto)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Reddito Reale Stefano", f"CHF {basis_stefano:,.0f}")
    st.progress(quote_stefano, text=f"Quota: {quote_stefano*100:.1f}%")
with col2:
    st.metric("Reddito Reale Stephanie", f"CHF {basis_stephanie:,.0f}")
    st.progress(quote_stephanie, text=f"Quota: {quote_stephanie*100:.1f}%")
with col3:
    st.metric("Potenza Familiare", f"CHF {total_basis:,.0f}")
    st.caption("Somma dei redditi netti reali")

st.divider()

# Sezione B: I Bonifici (Il cuore dell'app)
st.subheader("🚀 Lista Bonifici da Eseguire")

c_bonifici1, c_bonifici2 = st.columns(2)

with c_bonifici1:
    st.info("🧑🏻 **STEFANO VERSA:**")
    st.write(f"1. Assegni al C. Comune: **CHF {zulagen_stefano:.2f}**")
    st.write(f"2. Spese al C. Comune: **CHF {transfer_stefano_budget:,.2f}**")
    st.write(f"3. Rimborso a Stephanie: **CHF {schuld_stefano_total:,.2f}**")
    st.markdown(f"### Totale Uscite: CHF {zulagen_stefano + transfer_stefano_budget + schuld_stefano_total:,.2f}")

with c_bonifici2:
    st.success("👩🏼 **STEPHANIE VERSA:**")
    st.write(f"1. Assegni al C. Comune: **CHF {zulagen_stephanie:.2f}**")
    st.write(f"2. Spese al C. Comune: **CHF {transfer_stephanie_budget:,.2f}**")
    st.write("3. Rimborso: *(Riceve soldi da Stefano)*")
    st.markdown(f"### Totale Uscite: CHF {zulagen_stephanie + transfer_stephanie_budget:,.2f}")

st.divider()

# Sezione C: Tabella dettagliata
with st.expander("Vedi Tabella Riepilogativa per Excel"):
    df = pd.DataFrame({
        "Da Chi": ["Stefano", "Stephanie", "Stefano", "Stephanie", "Stefano"],
        "A Chi": ["C. Comune", "C. Comune", "C. Comune", "C. Comune", "Stephanie"],
        "Causale": ["Assegni", "Assegni", "Quota Spese", "Quota Spese", "Rimborso Salute"],
        "Importo": [zulagen_stefano, zulagen_stephanie, transfer_stefano_budget, transfer_stephanie_budget, schuld_stefano_total]
    })
    st.dataframe(df.style.format({"Importo": "{:.2f}"}), use_container_width=True, hide_index=True)
