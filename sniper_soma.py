import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - CENTRAL", layout="wide")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background-color: #161b22; border-radius: 10px; padding: 12px; 
        margin-top: 8px; border-left: 8px solid #00ff88;
        font-size: 18px; font-weight: bold;
    }
    .box-ferramenta {
        background: #0d1117; border: 1px solid #30363d; 
        padding: 20px; border-radius: 15px; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIAS INDEPENDENTES ---
if 'placar' not in st.session_state: st.session_state.placar = {"SG": 0, "LOSS": 0}
if 'mem_espelho' not in st.session_state: st.session_state.mem_espelho = []
if 'mem_pedra' not in st.session_state: st.session_state.mem_pedra = []
if 'mem_bear' not in st.session_state: st.session_state.mem_bear = []

# --- SIDEBAR (PLACAR) ---
with st.sidebar:
    st.header("📊 PLACAR SG")
    c1, c2 = st.columns(2)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("LOSS", st.session_state.placar["LOSS"])
    if st.button("✅ REGISTRAR SG"): 
        st.session_state.placar["SG"] += 1
        st.rerun()
    if st.button("❌ REGISTRAR LOSS"): 
        st.session_state.placar["LOSS"] += 1
        st.rerun()
    if st.button("🔄 ZERAR TUDO"): 
        st.session_state.placar = {"SG": 0, "LOSS": 0}
        st.session_state.mem_espelho = []
        st.session_state.mem_pedra = []
        st.session_state.mem_bear = []
        st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🎯 SNIPER MS - FERRAMENTAS")

tab1, tab2, tab3 = st.tabs(["💎 ESPELHO (3-9-12)", "🎲 PEDRA", "🎯 BEAR (4-2-3)"])

# --- ABA 1: ESPELHO ---
with tab1:
    st.markdown('<div class="box-ferramenta">', unsafe_allow_html=True)
    cor_00 = st.selectbox("Cor no minuto :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="c00")
    if st.button("🚀 GERAR LISTA ESPELHO", use_container_width=True):
        ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
        st.session_state.mem_espelho = []
        for p in [3, 9, 12]:
            h_s = ref + timedelta(minutes=p)
            st.session_state.mem_espelho.append({"h": h_s.strftime("%H:%M"), "c": cor_00})
    
    if st.session_state.mem_espelho:
        st.write("---")
        for s in st.session_state.mem_espelho:
            cor_c = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_c}">{s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 2: PEDRA ---
with tab2:
    st.markdown('<div class="box-ferramenta">', unsafe_allow_html=True)
    p_val = st.number_input("Número da Pedra:", 0, 14, 7)
    m_rel = st.number_input("Minuto Atual:", 0, 59, datetime.now(fuso_ms).minute)
    if st.button("🚀 CALCULAR POR PEDRA", use_container_width=True):
        m_calc = (p_val + m_rel) % 60
        st.session_state.mem_pedra = [{"h": f"Minuto :{m_calc:02d}", "c": "COR DO 00"}]
    
    if st.session_state.mem_pedra:
        st.write("---")
        for s in st.session_state.mem_pedra:
            st.markdown(f'<div class="card-sinal">{s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 3: BEAR ---
with tab3:
    st.markdown('<div class="box-ferramenta">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    h_b = c1.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
    m_b = c2.number_input("Minuto:", 0, 59, datetime.now(fuso_ms).minute)
    c_ini = st.selectbox("Cor Inicial:", ["VERMELHO 🔴", "PRETO ⚫"], key="cb")
    
    if st.button("🚀 GERAR SEQUÊNCIA BEAR", use_container_width=True):
        pulos = [0, 4, 2, 3, 4, 2]
        ref_b = datetime.now(fuso_ms).replace(hour=h_b, minute=m_b, second=0, microsecond=0)
        st.session_state.mem_bear = []
        c_at = c_ini
        for p in pulos:
            ref_b += timedelta(minutes=p)
            st.session_state.mem_bear.append({"h": ref_b.strftime("%H:%M"), "c": c_at})
            c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"
            
    if st.session_state.mem_bear:
        st.write("---")
        for s in st.session_state.mem_bear:
            cor_c = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_c}">{s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
