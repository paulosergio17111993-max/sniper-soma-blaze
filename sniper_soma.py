import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - BLOCOS", layout="wide")

# --- ESTILO VISUAL (QUADRADOS ORGANIZADOS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    /* Estilo do Quadrado da Ferramenta */
    .quadrado-ferramenta {
        background-color: #0d1117;
        border: 2px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border-top: 5px solid #6a5acd;
    }
    /* Estilo dos Sinais dentro do quadrado */
    .card-sinal { 
        background-color: #161b22; 
        border-radius: 8px; 
        padding: 10px; 
        margin-top: 5px; 
        border-left: 5px solid #00ff88;
        font-size: 16px;
    }
    .stButton>button { background-color: #6a5acd; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIAS ---
if 'mem' not in st.session_state:
    st.session_state.mem = {"espelho": [], "pedra": [], "bear": []}
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 PLACAR")
    st.metric("SG", st.session_state.placar["SG"])
    st.metric("LOSS", st.session_state.placar["LOSS"])
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()

st.title("🎯 SNIPER MS - SISTEMA DE BLOCOS")

# --- ORGANIZAÇÃO EM COLUNAS (QUADRADOS LADO A LADO OU EM TÓPICOS) ---
col1, col2 = st.columns(2)

# QUADRADO 1: ESPELHO
with col1:
    st.markdown('<div class="quadrado-ferramenta">', unsafe_allow_html=True)
    st.subheader("💎 PADRÃO ESPELHO")
    cor_00 = st.selectbox("Cor no :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="c1")
    if st.button("🚀 GERAR ESPELHO", use_container_width=True):
        ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
        st.session_state.mem["espelho"] = []
        for p in [3, 9, 12]:
            h = (ref + timedelta(minutes=p)).strftime("%H:%M")
            st.session_state.mem["espelho"].append(f"⏰ {h} | {cor_00}")
    
    for sinal in st.session_state.mem["espelho"]:
        st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# QUADRADO 2: CÁLCULO PEDRA
with col2:
    st.markdown('<div class="quadrado-ferramenta">', unsafe_allow_html=True)
    st.subheader("🎲 CÁLCULO PEDRA")
    p_v = st.number_input("Pedra:", 0, 14, 7)
    m_r = st.number_input("Minuto:", 0, 59, datetime.now(fuso_ms).minute)
    if st.button("🚀 CALCULAR PEDRA", use_container_width=True):
        m_c = (p_v + m_r) % 60
        st.session_state.mem["pedra"] = [f"⏰ Minuto :{m_c:02d} | ANALISAR"]
    
    for sinal in st.session_state.mem["pedra"]:
        st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# QUADRADO 3: PADRÃO BEAR (ABAIXO)
st.markdown('<div class="quadrado-ferramenta">', unsafe_allow_html=True)
st.subheader("🎯 PADRÃO BEAR (4-2-3)")
c1, c2, c3 = st.columns(3)
h_b = c1.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
m_b = c2.number_input("Minuto:", 0, 59, 10)
cor_b = c3.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="c3")

if st.button("🚀 GERAR SEQUÊNCIA BEAR", use_container_width=True):
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h_b), minute=int(m_b), second=0, microsecond=0)
    st.session_state.mem["bear"] = []
    c_at = cor_b
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.mem["bear"].append(f"⏰ {ref_b.strftime('%H:%M')} | {c_at}")
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"

# Exibe os sinais do Bear dentro do quadrado dele
cols_sinais = st.columns(3)
for i, sinal in enumerate(st.session_state.mem["bear"]):
    with cols_sinais[i % 3]:
        st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
