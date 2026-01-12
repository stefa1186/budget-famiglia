import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 0. CONFIGURAZIONE PAGINA
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Finanze Familiari v3", page_icon="🇨🇭", layout="wide")

# -----------------------------------------------------------------------------
# 1. INPUT (BARRA LATERALE - SINISTRA)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🔢 Dati Mensili")
    
    # --- SEZIONE REDDITI ---
    st.header("1. Stipendi")
    
    st.subheader("Stefano")
    lohn_stefano = st.number_input("Salario Versato (Netto)", value=8500.0, step=50.0, key="stef_sal")
    zulagen_stefano = st.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="stef_ass")
    
    st.subheader("Stephanie")
    lohn_stephanie = st.number_input("Salario Versato (Netto)", value=5000.0, step=50.0, key="steph_sal")
    zulagen_stephanie = st.number_input("di cui Assegni Familiari", value=250.0, step=50.0, key="steph_ass")
    
    st.markdown("---")
    
    # --- SEZIONE SALUTE ---
    st.header("2. Costi Salute (Stephanie)")
    st.info("Totale dedotto in busta paga")
    
    premi_kk = st.number_input("Premi Cassa Malati", value=1200.0, step=10.0, key="kk_premi")
    fatture_kk = st.number_input("Fatture Mediche", value=300.0, step=10.0, key="kk_fatt")
    total_abzug_kk = premi_kk + fatture_kk
    
    st.caption(f"Totale Dedotto: CHF {total_abzug_kk:,.2f}")
    
    st.markdown("**Ripartizione Costo:**")
    anteil_stefano_kk = st.number_input("Quota Stefano", value=500.0, step=10.0, key="q_stef")
    anteil_kinder_kk = st.number_input("Quota Figlie", value=500.0, step=10.0, key="q_kind")
    
    # Calcolo residuo Stephanie
    anteil_stephanie_kk = total_abzug_kk - anteil_stefano_kk - anteil_kinder_kk
    if anteil_stephanie_kk < -0.1:
        st.error(f"Errore! Quote > Totale.")
    else:
        st.caption(f"Quota Stephanie: CHF {anteil_stephanie_kk:.2f}")

    st.markdown("---")

    # --- SEZIONE BUDGET (NUOVA) ---
    st.header("3. Spese Comuni")
    
    costo_affitto = st.number_input("Affitto & Spese", value=3000.0, step=50.0, key="costo_affitto")
    costo_krippe = st.number_input("Kinderkrippe (Nido)", value=2500.0, step=50.0, key="costo_krippe")
    costo_spese = st.number_input("Spese Generali (Cibo/Ferie)", value=1500.0, step=50.0, key="costo_spese")
    
    # Somma automatica
    budget_ziel = costo_affitto + costo_krippe + costo_spese
    st.markdown(f"### Totale: CHF {budget_ziel:,.2f}")

# -----------------------------------------------------------------------------
# 2. LOGICA DI CALCOLO
# -----------------------------------------------------------------------------

# A. Reddito Reale (Ricostruzione imponibile)
basis_stefano = lohn_stefano - zulagen_stefano
basis_stephanie = (lohn_stephanie - zulagen_stephanie) + total_abzug_kk
total_basis = basis_stefano + basis_stephanie

# B. Ratio (Percentuali)
if total_basis > 0:
    quote_stefano = basis_stefano / total_basis
    quote_stephanie = basis_stephanie / total_basis
else:
    quote_stefano = 0.5
    quote_stephanie = 0.5

# C. Finanziamento Budget
total_zulagen = zulagen_stefano + zulagen_stephanie
restfinanzierung = budget_ziel - total_zulagen

transfer_stefano_budget = restfinanzierung * quote_stefano
transfer_stephanie_budget = restfinanzierung * quote_stephanie

# D. Debito Salute (Rimborso privato)
schuld_stefano_total = anteil_stefano_kk + (anteil_kinder_kk * quote_stefano)

# -----------------------------------------------------------------------------
# 3. OUTPUT (DASHBOARD)
# -----------------------------------------------------------------------------

st.title("🇨🇭 Gestione Finanze: Stefano & Stephanie")

# --- RIEPILOGO VISIVO ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Reddito Reale Stefano", f"CHF {basis_stefano:,.0f}")
    st.progress(quote_stefano, text=f"{quote_stefano*100:.1f}%")
with col2:
    st.metric("Reddito Reale Stephanie", f"CHF {basis_stephanie:,.0f}")
    st.progress(quote_stephanie, text=f"{quote_stephanie*100:.1f}%")
with col3:
    st.metric("Budget Comune Totale", f"CHF {budget_ziel:,.0f}")
    st.caption(f"Affitto: {costo_affitto:.0f} | Krippe: {costo_krippe:.0f} | Spese: {costo_spese:.0f}")
with col4:
    st.metric("Da finanziare (No Assegni)", f"CHF {restfinanzierung:,.0f}", delta=f"- CHF {total_zulagen:.0f} Assegni", delta_color="off")

st.divider()

# --- I BONIFICI ---
st.subheader("🚀 Lista Bonifici da Eseguire")

col_left, col_right = st.columns(2)

# Colonna STEFANO
with col_left:
    st.info("🧑🏻 **STEFANO VERSA:**")
    st.markdown(f"""
    1.  **Assegni** $\\to$ Conto Comune: `CHF {zulagen_stefano:.2f}`
    2.  **Spese ({quote_stefano*100:.1f}%)** $\\to$ Conto Comune: `CHF {transfer_stefano_budget:,.2f}`
    3.  **Salute** $\\to$ Stephanie: `CHF {schuld_stefano_total:,.2f}`
    """)
    tot_stefano = zulagen_stefano + transfer_stefano_budget + schuld_stefano_total
    st.markdown(f"### Totale Uscite: CHF {tot_stefano:,.2f}")

# Colonna STEPHANIE
with col_right:
    st.success("👩🏼 **STEPHANIE VERSA:**")
    st.markdown(f"""
    1.  **Assegni** $\\to$ Conto Comune: `CHF {zulagen_stephanie:.2f}`
    2.  **Spese ({quote_stephanie*100:.1f}%)** $\\to$ Conto Comune: `CHF {transfer_stephanie_budget:,.2f}`
    3.  **Salute**: *(Riceve rimborso da Stefano)*
    """)
    tot_stephanie = zulagen_stephanie + transfer_stephanie_budget
    st.markdown(f"### Totale Uscite: CHF {tot_stephanie:,.2f}")

st.divider()

# --- TABELLA RIEPILOGATIVA ---
with st.expander("📋 Tabella Dettagliata (Copia per Excel/Archivio)"):
    df = pd.DataFrame({
        "Da Chi": ["Stefano", "Stephanie", "Stefano", "Stephanie", "Stefano"],
        "A Chi": ["C. Comune", "C. Comune", "C. Comune", "C. Comune", "Stephanie"],
        "Causale": ["Assegni", "Assegni", "Quota Spese", "Quota Spese", "Rimborso Salute"],
        "Importo (CHF)": [zulagen_stefano, zulagen_stephanie, transfer_stefano_budget, transfer_stephanie_budget, schuld_stefano_total]
    })
    st.dataframe(df.style.format({"Importo (CHF)": "{:.2f}"}), use_container_width=True, hide_index=True)
    
    st.markdown("#### Dettaglio Rimborso Salute (S -> S)")
    st.markdown(f"""
    * Quota Stefano (100%): CHF {anteil_stefano_kk:.2f}
    * Quota Figlie ({quote_stefano*100:.1f}% di {anteil_kinder_kk}): CHF {anteil_kinder_kk * quote_stefano:.2f}
    * **Totale**: CHF {schuld_stefano_total:.2f}
    """)
