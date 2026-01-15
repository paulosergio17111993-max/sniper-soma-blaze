import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL GAMER EXTREME ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #e0e0e0; }
    
    /* Blocos Cinzas Limpos */
    .topico-bloco {
        background: linear-gradient(145deg, #0d1117, #161b22);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 35px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
        border-top: 5px solid #6a5acd;
    }
    
    /* Cards de Sinais */
    .card-sinal { 
        background: #1c2128;
        border-radius: 12px;
        padding: 15px;
        margin-top: 10px;
        border-left: 5px solid #00ff88;
        font-weight: bold;
        text-align: center;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.4);
    }
    
    /* Botão Roxo Gamer */
    .stButton>button { 
        background: linear-gradient(90deg, #6a5acd, #8a2be2) !important;
        color: white !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        width: 100%;
        height: 3.8em;
        border-radius: 15px;
        border: none;
        text-transform: uppercase;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 25px rgba(106, 90, 205, 0.5); }

    /* Inputs Brancos Profissionais */
    div[data-baseweb="input"] { background-color: white !important; border-radius: 10px !important; }
    input { color: black !important; font-weight: bold !important; font-size: 1.1rem !important; }
    label { color: #6a5acd !important; font-weight: 800 !important; font-size: 1rem !important; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN VIP ---
if 'autenticado' not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown('<div class="topico-bloco" style="max-width: 450px; margin: 100px auto; text-align: center;">', unsafe_allow_html=True)
    st.title("🚀 ACESSO VIP")
    senha = st.text_input("DIGITE A SENHA:", type="password")
    if st.button("LIBERAR"):
        if senha == "vip777":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("SENHA INVÁLIDA")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- MEMÓRIA ---
if 'L1' not in st.session_state: st.session_state.L1 = [] 
if 'L2' not in st.session_state: st.session_state.L2 = [] 

st.markdown("<h1 style='text-align: center; color: #6a5acd; font-size: 3rem; margin-bottom: 50px;'>🎯 SNIPER MS PRO</h1>", unsafe_allow_html=True)

# --- BLOCO 1: SEQUÊNCIA 3-6 (NOME REMOVIDO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns(3)
h_in = col_a.number_input("HORA:", 0, 23, 14)
m_in = col_b.number_input("MINUTO:", 0, 59, 9)
cor_sel = col_c.selectbox("COR DE ENTRADA:", ["PRETO ⚫", "VERMELHO 🔴"], key="cor1")

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

# --- BLOCO 2: PADRÃO 4-2-3 (NOME REMOVIDO) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
col_d, col_e = st.columns(2)
h4 = col_d.number_input("HORA DA RODADA:", 0, 23, datetime.now(fuso_ms).hour, key="h4")
cor4 = col_e.selectbox("COR INICIAL:", ["VERMELHO 🔴", "PRETO ⚫"], key="c4")

if st.button("🚀 GERAR PADRÃO 4-2-3", key="btn2"):
    st.session_state.L2 = []
    pulos = [0, 4, 2, 3, 4, 2]
    # Padrão começa no minuto 00 da hora escolhida
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
