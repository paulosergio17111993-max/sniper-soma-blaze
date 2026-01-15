import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - CENTRAL", layout="wide")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background-color: #161b22; border-radius: 10px; padding: 12px; 
        margin-top: 8px; border-left: 8px solid #00ff88;
        font-size: 18px; font-weight: bold; color: white;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #6a5acd; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIAS (Cada uma na sua caixa) ---
if 'placar' not in st.session_state: st.session_state.placar = {"SG": 0, "LOSS": 0}
if 'lista_espelho' not in st.session_state: st.session_state.lista_espelho = []
if 'lista_pedra' not in st.session_state: st.session_state.lista_pedra = []
if 'lista_bear' not in st.session_state: st.session_state.lista_bear = []

# --- BARRA LATERAL (PLACAR) ---
with st.sidebar:
    st.header("📊 PLACAR SG")
    c1, c2 = st.columns(2)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("LOSS", st.session_state.placar["LOSS"])
    st.markdown("---")
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()
    if st.button("🔄 ZERAR TUDO"): 
        st.session_state.placar = {"SG": 0, "LOSS": 0}
        st.session_state.lista_espelho = []
        st.session_state.lista_pedra = []
        st.session_state.lista_bear = []
        st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🎯 SNIPER MS - CENTRAL")

tab1, tab2, tab3 = st.tabs(["💎 ESPELHO (3-9-12)", "🎲 PEDRA", "🎯 BEAR (4-2-3)"])

# --- ABA 1: ESPELHO ---
with tab1:
    st.subheader("🕵️ Lógica do Minuto :00")
    cor_00 = st.selectbox("Cor no minuto :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="c00")
    if st.button("🚀 GERAR LISTA ESPELHO", key="btn_e"):
        ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
        st.session_state.lista_espelho = []
        for p in [3, 9, 12]:
            h_s = ref + timedelta(minutes=p)
            st.session_state.lista_espelho.append({"h": h_s.strftime("%H:%M"), "c": cor_00})
    
    # RESULTADO ABAIXO DO BOTÃO (DENTRO DA ABA)
    if st.session_state.lista_espelho:
        st.markdown("---")
        for s in st.session_state.lista_espelho:
            cor_b = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_b}">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)

# --- ABA 2: PEDRA ---
with tab2:
    st.subheader("🎲 Cálculo por Pedra")
    p_v = st.number_input("Número da Pedra:", 0, 14, 7)
    m_r = st.number_input("Minuto do Relógio:", 0, 59, datetime.now(fuso_ms).minute)
    if st.button("🚀 GERAR LISTA PEDRA", key="btn_p"):
        m_c = (p_v + m_r) % 60
        st.session_state.lista_pedra = [{"h": f"Minuto :{m_c:02d}", "c": "ANALISANDO"}]
    
    # RESULTADO ABAIXO DO BOTÃO (DENTRO DA ABA)
    if st.session_state.lista_pedra:
        st.markdown("---")
        for s in st.session_state.lista_pedra:
            st.markdown(f'<div class="card-sinal">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)

# --- ABA 3: BEAR ---
with tab3:
    st.subheader("🎯 Padrão Bear (4-2-3)")
    c_h, c_m = st.columns(2)
    h_b = c_h.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
    m_b = c_m.number_input("Minuto Inicial:", 0, 59, datetime.now(fuso_ms).minute)
    c_i = st.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="cb")
    
    if st.button("🚀 GERAR LISTA BEAR", key="btn_b"):
        pulos = [0, 4, 2, 3, 4, 2]
        ref_b = datetime.now(fuso_ms).replace(hour=int(h_b), minute=int(m_b), second=0, microsecond=0)
        st.session_state.lista_bear = []
        c_at = c_i
        for p in pulos:
            ref_b += timedelta(minutes=p)
            st.session_state.lista_bear.append({"h": ref_b.strftime("%H:%M"), "c": c_at})
            c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"
            
    # RESULTADO ABAIXO DO BOTÃO (DENTRO DA ABA)
    if st.session_state.lista_bear:
        st.markdown("---")
        for s in st.session_state.lista_bear:
            cor_b = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_b}">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
