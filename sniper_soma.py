import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL (QUADRADOS SEPARADOS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .topico-bloco {
        background-color: #0d1117; border: 2px solid #30363d;
        border-radius: 15px; padding: 20px; margin-bottom: 25px;
        border-top: 5px solid #6a5acd;
    }
    .card-sinal { 
        background-color: #161b22; border-radius: 8px; padding: 12px; 
        margin-top: 8px; border-left: 5px solid #00ff88; font-weight: bold;
    }
    .stButton>button { 
        background-color: #6a5acd; color: white; font-weight: bold; 
        width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA INDEPENDENTE (PARA NÃO SUMIR) ---
if 'L1' not in st.session_state: st.session_state.L1 = [] # Memória do Padrão 1
if 'L2' not in st.session_state: st.session_state.L2 = [] # Memória do Padrão 4-2-3

# --- PLACAR ---
with st.sidebar:
    st.header("📊 PLACAR")
    if 'sg' not in st.session_state: st.session_state.sg = 0
    if 'ls' not in st.session_state: st.session_state.ls = 0
    st.metric("SG", st.session_state.sg)
    st.metric("LOSS", st.session_state.ls)
    if st.button("✅ REGISTRAR SG"): st.session_state.sg += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.ls += 1; st.rerun()
    if st.button("🔄 ZERAR TUDO"): 
        st.session_state.L1 = []; st.session_state.L2 = []; st.session_state.sg = 0; st.session_state.ls = 0
        st.rerun()

st.title("🎯 SNIPER MS - FERRAMENTAS FIXAS")

# --- QUADRADO 1: PADRÃO DE SEQUÊNCIA (3 e 6 MINUTOS) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO DE SEQUÊNCIA (EXATO)")
c1, c2, c3 = st.columns(3)
h_in = c1.number_input("Hora:", 0, 23, 14)
m_in = c2.number_input("Minuto:", 0, 59, 30)
cor_sel = c3.selectbox("Cor:", ["PRETO ⚫", "VERMELHO 🔴"], key="cor1")

if st.button("🚀 GERAR LISTA", key="btn_lista"):
    st.session_state.L1 = []
    # Padrão da sua lista: 30, 33, 39, 42, 45, 48, 51, 54, 57
    pulos_exatos = [0, 3, 6, 3, 3, 3, 3, 3, 3] 
    ref = datetime.now(fuso_ms).replace(hour=int(h_in), minute=int(m_in), second=0, microsecond=0)
    
    acumulado = 0
    for p in pulos_exatos:
        acumulado += p
        horario = (ref + timedelta(minutes=acumulado)).strftime("%H:%M")
        st.session_state.L1.append(f"⏰ {horario} | {cor_sel}")

# Exibe a lista 1 (Não some quando clica no outro botão)
if st.session_state.L1:
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.L1):
        with cols[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- QUADRADO 2: PADRÃO 4-2-3 ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 2. PADRÃO 4-2-3")
c4, c5, c6 = st.columns(3)
h4 = c4.number_input("Hora:", 0, 23, 21, key="h4")
m4 = c5.number_input("Minuto:", 0, 59, 2, key="m4")
cor4 = c6.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="c4")

if st.button("🚀 GERAR LISTA", key="btn_423"):
    st.session_state.L2 = []
    pulos_423 = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h4), minute=int(m4), second=0, microsecond=0)
    cor_at = cor4
    for p in pulos_423:
        ref_b += timedelta(minutes=p)
        st.session_state.L2.append(f"⏰ {ref_b.strftime('%H:%M')} | {cor_at}")
        cor_at = "PRETO ⚫" if cor_at == "VERMELHO 🔴" else "VERMELHO 🔴"

# Exibe a lista 2 (Não some quando clica no outro botão)
if st.session_state.L2:
    cols_b = st.columns(3)
    for i, s in enumerate(st.session_state.L2):
        with cols_b[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
