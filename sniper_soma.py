import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="SOMA PRO - GAMER EDITION", layout="centered")

# --- VISUAL GAME TOP (CSS NEON & DARK) ---
st.markdown("""
    <style>
    /* Fundo principal com degradê escuro */
    .stApp {
        background: radial-gradient(circle, #1a1a2e 0%, #0f0f1a 100%);
        color: #00f2ff;
    }
    
    /* Estilo dos Títulos */
    h1 {
        text-shadow: 0 0 10px #7000ff, 0 0 20px #7000ff;
        color: #fff;
        font-family: 'Courier New', Courier, monospace;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    /* Botões Gamer */
    .stButton>button {
        background: linear-gradient(90deg, #7000ff, #00f2ff);
        color: white !important;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
        text-transform: uppercase;
        transition: 0.3s;
        box-shadow: 0 0 15px rgba(112, 0, 255, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.8);
        transform: scale(1.05);
    }

    /* Card de Sinal Único (Neon Pulsante) */
    .alerta-soma {
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #7000ff;
        box-shadow: 0 0 20px #7000ff;
        margin-bottom: 25px;
    }

    /* Cards das Listas (Visual Glassmorphism) */
    .card-geral {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(0, 242, 255, 0.3);
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .estrelas { color: #ff00c8; text-shadow: 0 0 5px #ff00c8; }
    
    /* Inputs */
    .stNumberInput label { color: #00f2ff !important; font-weight: bold; }
    input { background-color: #000 !important; color: #00f2ff !important; border: 1px solid #7000ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if not st.session_state.autenticado:
    st.markdown("<h1>⚡ ACESSO VIP ⚡</h1>", unsafe_allow_html=True)
    senha = st.text_input("DIGITE A CHAVE DE ACESSO:", type="password")
    if st.button("DESBLOQUEAR TERMINAL"):
        if senha == "VIP777":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- MEMÓRIA DO PAINEL ---
if 'exibir_soma' not in st.session_state: st.session_state.exibir_soma = False
if 'exibir_cores' not in st.session_state: st.session_state.exibir_cores = False
if 'exibir_branco' not in st.session_state: st.session_state.exibir_branco = False

# --- INTERFACE ---
st.markdown("<h1>🎮 SOMA PRO v3.0</h1>", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        pedra = st.number_input("ÚLTIMA PEDRA:", 0, 14, step=1)
    with col2:
        min_atual = st.number_input("MINUTO ATUAL:", 0, 59, step=1)

# Lógica de Horário
fuso = pytz.timezone('America/Sao_Paulo')
agora = datetime.datetime.now(fuso)
intervalos = [4, 8, 12, 16, 20]

st.write("---")

# --- BOTÕES DE COMANDO ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔥 SOMA PEDRA"): st.session_state.exibir_soma = True
with c2:
    if st.button("📋 LISTA CORES"): st.session_state.exibir_cores = True
with c3:
    if st.button("⚪ LISTA BRANCO"): st.session_state.exibir_branco = True

if st.button("❌ RESETAR SISTEMA"):
    st.session_state.exibir_soma = st.session_state.exibir_cores = st.session_state.exibir_branco = False
    st.rerun()

# --- EXIBIÇÃO ---

if st.session_state.exibir_soma:
    min_soma = (pedra + min_atual) % 60
    if 1 <= pedra <= 7:
        c_nome, c_hex = "VERMELHO 🔴", "#ff4b4b"
    elif pedra >= 8:
        c_nome, c_hex = "PRETO ⚫", "#1d1d1d"
    else:
        c_nome, c_hex = "BRANCO ⚪", "#ffffff"
        
    st.markdown(f"""
        <div class="alerta-soma">
            <p style="letter-spacing: 2px; color: #00f2ff;">[ ANALISANDO PADRÃO... ]</p>
            <h1 style="color: {c_hex}; filter: drop-shadow(0 0 10px {c_hex});">{c_nome}</h1>
            <h2 style="font-size: 40px; margin: 10px 0;">MINUTO: {min_soma:02d}</h2>
            <p style="color: #7000ff;">PROTEÇÃO NO BRANCO ATIVADA</p>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.exibir_branco:
    st.markdown("<h3 style='color: #fff;'>⚪ SCANNER DE BRANCOS</h3>", unsafe_allow_html=True)
    for t in intervalos:
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span style="color: #fff;">BRANCO ⚪</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)

if st.session_state.exibir_cores:
    st.markdown("<h3 style='color: #00f2ff;'>📋 RADAR DE CORES</h3>", unsafe_allow_html=True)
    for i, t in enumerate(intervalos):
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        c_txt, c_hex = ("VERMELHO 🔴", "#ff4b4b") if i % 2 == 0 else ("PRETO ⚫", "#555")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span style="color:{c_hex}">{c_txt}</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; font-size:10px; margin-top:50px;'>CONEXÃO ENCRIPTADA - SOMA PRO V3</p>", unsafe_allow_html=True)
