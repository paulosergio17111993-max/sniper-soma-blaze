import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL ---
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

# --- SISTEMA DE MEMÓRIA GLOBAL (IMPEDE QUE AS COISAS SUMAM) ---
if 'placar_sg' not in st.session_state: st.session_state.placar_sg = 0
if 'placar_loss' not in st.session_state: st.session_state.placar_loss = 0
if 'L1' not in st.session_state: st.session_state.L1 = [] # Gaveta Espelho
if 'L2' not in st.session_state: st.session_state.L2 = [] # Gaveta Soma
if 'L3' not in st.session_state: st.session_state.L3 = [] # Gaveta 4-2-3

# --- BARRA LATERAL (PLACAR INDEPENDENTE) ---
with st.sidebar:
    st.header("📊 PLACAR SG")
    st.metric("SG", st.session_state.placar_sg)
    st.metric("LOSS", st.session_state.placar_loss)
    if st.button("✅ REGISTRAR SG"): 
        st.session_state.placar_sg += 1
        st.rerun()
    if st.button("❌ REGISTRAR LOSS"): 
        st.session_state.placar_loss += 1
        st.rerun()
    if st.button("🔄 LIMPAR TUDO"):
        st.session_state.L1 = []; st.session_state.L2 = []; st.session_state.L3 = []
        st.session_state.placar_sg = 0; st.session_state.placar_loss = 0
        st.rerun()

st.title("🎯 SNIPER MS - CENTRAL")

# --- 1. QUADRADO ESPELHO ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO ESPELHO (3-9-12)")
c_esp = st.selectbox("Cor do :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="sel_e")
if st.button("🚀 GERAR LISTA", key="btn_e"):
    ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
    st.session_state.L1 = []
    for p in [3, 9, 12]:
        h = (ref + timedelta(minutes=p)).strftime("%H:%M")
        st.session_state.L1.append(f"⏰ {h} | {c_esp}")

for s in st.session_state.L1:
    st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. QUADRADO SOMA (PEDRA + MINUTO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎲 2. CÁLCULO SOMA (PEDRA + MINUTO)")
pedra = st.number_input("Pedra (0-14):", 0, 14, 7, key="num_p")
if st.button("🚀 GERAR LISTA", key="btn_s"):
    m_atual = datetime.now(fuso_ms).minute
    res_soma = (pedra + m_atual) % 60
    st.session_state.L2 = [f"⏰ Minuto :{res_soma:02d} | ENTRAR NA COR DO :00"]

for s in st.session_state.L2:
    st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. QUADRADO PADRÃO 4-2-3 ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 3. PADRÃO 4-2-3")
col1, col2 = st.columns(2)
h_423 = col1.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour, key="h_4")
m_423 = col2.number_input("Minuto:", 0, 59, 10, key="m_4")
cor_423 = st.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="c_4")

if st.button("🚀 GERAR LISTA", key="btn_b"):
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h_423), minute=int(m_423), second=0, microsecond=0)
    st.session_state.L3 = []
    c_at = cor_423
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.L3.append(f"⏰ {ref_b.strftime('%H:%M')} | {c_at}")
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"

# Exibe em colunas para ficar bonito
if st.session_state.L3:
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.L3):
        with cols[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
