import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL (QUADRADOS IGUAIS ÀS FOTOS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .topico-bloco {
        background-color: #0d1117; border: 2px solid #30363d;
        border-radius: 15px; padding: 20px; margin-bottom: 25px;
        border-top: 5px solid #6a5acd;
    }
    .card-sinal { 
        background-color: #161b22; border-radius: 8px; padding: 10px; 
        margin-top: 5px; border-left: 5px solid #00ff88; font-weight: bold;
    }
    /* Botão Roxo com texto Gerar Lista */
    .stButton>button { 
        background-color: #6a5acd; color: white; font-weight: bold; 
        width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA (NÃO APAGA AO MUDAR) ---
if 'mem' not in st.session_state:
    st.session_state.mem = {"espelho": [], "pedra": [], "padrao_423": []}
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- BARRA LATERAL (PLACAR) ---
with st.sidebar:
    st.header("📊 PLACAR SG")
    st.metric("SG", st.session_state.placar["SG"])
    st.metric("LOSS", st.session_state.placar["LOSS"])
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()
    if st.button("🔄 ZERAR TUDO"): 
        st.session_state.placar = {"SG": 0, "LOSS": 0}
        st.session_state.mem = {"espelho": [], "pedra": [], "padrao_423": []}
        st.rerun()

st.title("🎯 SNIPER MS - SISTEMA DE TÓPICOS")

# --- TÓPICO 1: ESPELHO (3 EM 3 MINUTOS - HORA TODA) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO ESPELHO (3-9-12)")
col_e1, col_e2 = st.columns(2)
h_sel = col_e1.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
c_sel = col_e2.selectbox("Cor do :00:", ["PRETO ⚫", "VERMELHO 🔴"])

if st.button("🚀 GERAR LISTA", key="btn_esp"):
    # Gera a sequência de 3 em 3 minutos para a hora toda
    ref = datetime.now(fuso_ms).replace(hour=int(h_sel), minute=0, second=0, microsecond=0)
    st.session_state.mem["espelho"] = []
    for m in range(0, 60, 3):
        h_s = (ref + timedelta(minutes=m)).strftime("%H:%M")
        st.session_state.mem["espelho"].append(f"⏰ {h_s} | {c_sel}")

# Mostra em 4 colunas para caber tudo no quadrado
if st.session_state.mem["espelho"]:
    cols = st.columns(4)
    for i, s in enumerate(st.session_state.mem["espelho"]):
        with cols[i % 4]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- TÓPICO 2: PEDRA (CÁLCULO DIRETO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎲 2. CÁLCULO POR PEDRA")
p_val = st.number_input("Número da Pedra:", 0, 14, 7)
if st.button("🚀 GERAR LISTA", key="btn_ped"):
    m_atual = datetime.now(fuso_ms).minute
    m_calc = (p_val + m_atual) % 60
    st.session_state.mem["pedra"] = [f"⏰ Minuto :{m_calc:02d} | ENTRAR"]

for s in st.session_state.mem["pedra"]:
    st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- TÓPICO 3: PADRÃO 4-2-3 (SEQUÊNCIA COMPLETA) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 3. PADRÃO 4-2-3")
col_b1, col_b2, col_b3 = st.columns(3)
h_b = col_b1.number_input("Hora Início:", 0, 23, datetime.now(fuso_ms).hour, key="h423")
m_b = col_b2.number_input("Minuto Início:", 0, 59, 10, key="m423")
c_b = col_b3.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="c423")

if st.button("🚀 GERAR LISTA", key="btn_423"):
    pulos = [0, 4, 2, 3, 4, 2] # Padrão das fotos
    ref_b = datetime.now(fuso_ms).replace(hour=int(h_b), minute=int(m_b), second=0, microsecond=0)
    st.session_state.mem["padrao_423"] = []
    cor_at = c_b
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.mem["padrao_423"].append(f"⏰ {ref_b.strftime('%H:%M')} | {cor_at}")
        cor_at = "PRETO ⚫" if cor_at == "VERMELHO 🔴" else "VERMELHO 🔴"

if st.session_state.mem["padrao_423"]:
    cols_b = st.columns(3)
    for i, s in enumerate(st.session_state.mem["padrao_423"]):
        with cols_b[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
