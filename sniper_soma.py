import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL GAMER ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    .topico-bloco {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 30px;
        border-top: 4px solid #6a5acd;
    }
    .card-sinal { 
        background: #1c2128;
        border-radius: 12px;
        padding: 15px;
        margin-top: 10px;
        border-left: 5px solid #00ff88;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button { 
        background: linear-gradient(90deg, #6a5acd, #8a2be2);
        color: white !important;
        font-weight: 800;
        width: 100%;
        height: 3.5em;
        border-radius: 12px;
        border: none;
        text-transform: uppercase;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; }
    label { color: #6a5acd !important; font-weight: bold !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SENHA ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<div class="topico-bloco" style="max-width: 450px; margin: 100px auto; text-align: center;">', unsafe_allow_html=True)
    st.title("🔐 LOGIN SNIPER")
    senha = st.text_input("SENHA DE ACESSO:", type="password")
    if st.button("LIBERAR ACESSO"):
        if senha == "vip777":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("SENHA INCORRETA")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- MEMÓRIA ---
if 'L1' not in st.session_state: st.session_state.L1 = [] 
if 'L2' not in st.session_state: st.session_state.L2 = [] 

st.markdown("<h1 style='text-align: center; color: #6a5acd; margin-bottom: 40px;'>🎯 SNIPER MS PRO</h1>", unsafe_allow_html=True)

# --- QUADRADO 1: SEQUÊNCIA 3-6 (LIMPO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
h_in = c1.number_input("HORA:", 0, 23, 14)
m_in = c2.number_input("MINUTO INICIAL:", 0, 59, 9)
cor_sel = c3.selectbox("COR:", ["PRETO ⚫", "VERMELHO 🔴"], key="cor1")

if st.button("🚀 GERAR LISTA COMPLETA", key="btn1"):
    st.session_state.L1 = []
    ref = datetime.now(fuso_ms).replace(hour=int(h_in), minute=int(m_in), second=0, microsecond=0)
    t_atual = ref
    st.session_state.L1.append(f"⏰ {t_atual.strftime('%H:%M')} | {cor_sel}")
    for i in range(29):
        pulo = 3 if i % 2 == 0 else 6
        t_atual += timedelta(minutes=pulo)
        st.session_state.L1.append(f"⏰ {t_atual.strftime('%H:%M')} | {cor_sel}")

if st.session_state.L1:
    cols = st.columns(5)
    for i, s in enumerate(st.session_state.L1):
        with cols[i % 5]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- QUADRADO 2: PADRÃO 4-2-3 (LIMPO E SEM MINUTO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
c4, c5 = st.columns(2)
h4 = c4.number_input("HORA DE OPERAÇÃO:", 0, 23, datetime.now(fuso_ms).hour, key="h4")
cor4 = c5.selectbox("ESCOLHA A COR:", ["VERMELHO 🔴", "PRETO ⚫"], key="c4")

if st.button("🚀 GERAR PADRÃO 4-2-3", key="btn2"):
    st.session_state.L2 = []
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h4), minute=0, second=0, microsecond=0)
    c_at = cor4
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.L2.append(f"⏰ {ref_b.strftime('%H:%M')} | {c_at}")
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"

if st.session_state.L2:
    cols_b = st.columns(3)
    for i, s in enumerate(st.session_state.L2):
        with cols_b[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
