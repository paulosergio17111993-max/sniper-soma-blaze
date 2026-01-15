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
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        border-top: 4px solid #6a5acd;
    }
    .card-sinal { 
        background: #161b22;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border-left: 5px solid #00ff88;
        font-weight: bold;
        text-align: center;
    }
    .card-branco { 
        background: #1c2128;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border-left: 5px solid #ffffff;
        color: #ffffff;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button { 
        background: #6a5acd !important;
        color: white !important;
        font-weight: bold !important;
        width: 100%;
        height: 3.5em;
        border-radius: 12px;
        border: none;
        text-transform: uppercase;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; }
    label { color: #6a5acd !important; font-weight: 900 !important; font-size: 0.9rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN (vip777) ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False
if not st.session_state.autenticado:
    st.markdown('<div class="topico-bloco" style="max-width: 400px; margin: 100px auto; text-align: center;">', unsafe_allow_html=True)
    st.title("🔐 ACESSO")
    senha = st.text_input("SENHA:", type="password")
    if st.button("ENTRAR"):
        if senha == "vip777":
            st.session_state.autenticado = True
            st.rerun()
        else: st.error("ERRO")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- MEMÓRIA (NÃO MEXE NAS OUTRAS) ---
if 'L1' not in st.session_state: st.session_state.L1 = [] 
if 'L2' not in st.session_state: st.session_state.L2 = [] 
if 'L3' not in st.session_state: st.session_state.L3 = [] 

st.markdown("<h1 style='text-align: center; color: white;'>🏹 SNIPER MS PRO</h1>", unsafe_allow_html=True)

# --- QUADRADO 1 (SEQUÊNCIA 3-6) - IGUALZINHO ANTES ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
h_in = c1.number_input("HORA:", 0, 23, 14, key="h1")
m_in = c2.number_input("MINUTO:", 0, 59, 9, key="m1")
cor_sel = c3.selectbox("COR:", ["PRETO ⚫", "VERMELHO 🔴"], key="cor1")
if st.button("🚀 GERAR LISTA", key="btn1"):
    st.session_state.L1 = []
    ref = datetime.now(fuso_ms).replace(hour=int(h_in), minute=int(m_in), second=0, microsecond=0)
    t_at = ref
    st.session_state.L1.append(f"⏰ {t_at.strftime('%H:%M')} | {cor_sel}")
    for i in range(29):
        pulo = 3 if i % 2 == 0 else 6
        t_at += timedelta(minutes=pulo)
        st.session_state.L1.append(f"⏰ {t_at.strftime('%H:%M')} | {cor_sel}")
if st.session_state.L1:
    cols = st.columns(5)
    for i, s in enumerate(st.session_state.L1):
        with cols[i % 5]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- QUADRADO 2 (PADRÃO 4-2-3) - IGUALZINHO ANTES ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
c4, c5 = st.columns(2)
h4 = c4.number_input("HORA DA RODADA:", 0, 23, 21, key="h4")
cor4 = c5.selectbox("COR INICIAL:", ["VERMELHO 🔴", "PRETO ⚫"], key="c4")
if st.button("🚀 GERAR LISTA", key="btn2"):
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

# --- QUADRADO 3 (NOVO: TERMINAIS DE BRANCO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
c6 = st.columns(1)[0]
h_br = c6.number_input("HORA DO BRANCO:", 0, 23, 9, key="h_br")
if st.button("🚀 GERAR LISTA", key="btn3"):
    st.session_state.L3 = []
    # Terminais fortes baseados na sua análise (filtrando 4 e 11)
    term_fortes = [0, 2, 3, 5, 9, 14, 15, 23, 24, 33, 35, 44, 51, 54, 56]
    for t in term_fortes:
        st.session_state.L3.append(f"⚪ {h_br:02d}:{t:02d}")
if st.session_state.L3:
    cols_br = st.columns(4)
    for i, s in enumerate(st.session_state.L3):
        with cols_br[i % 4]: st.markdown(f'<div class="card-branco">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
