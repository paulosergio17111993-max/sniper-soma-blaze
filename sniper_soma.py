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
        background-color: #161b22; border-radius: 8px; padding: 10px; 
        margin-top: 5px; border-left: 5px solid #00ff88; font-weight: bold;
    }
    .stButton>button { background-color: #6a5acd; color: white; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'mem' not in st.session_state:
    st.session_state.mem = {"espelho": [], "pedra": [], "padrao_423": []}
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📊 PLACAR")
    st.metric("SG", st.session_state.placar["SG"])
    st.metric("LOSS", st.session_state.placar["LOSS"])
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()

st.title("🎯 SNIPER MS - OPERAÇÃO CONTÍNUA")

# --- TÓPICO 1: ESPELHO (AGORA COM HORA TODA) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO ESPELHO (HORA COMPLETA)")
col_e1, col_e2 = st.columns(2)
h_ref = col_e1.number_input("Hora de Início:", 0, 23, datetime.now(fuso_ms).hour)
c_esp = col_e2.selectbox("Cor de Referência:", ["PRETO ⚫", "VERMELHO 🔴"])

if st.button("🚀 GERAR LISTA DA HORA TODA"):
    # Lógica para gerar de 3 em 3 minutos para a hora inteira
    ref = datetime.now(fuso_ms).replace(hour=int(h_ref), minute=0, second=0, microsecond=0)
    st.session_state.mem["espelho"] = []
    
    for minuto in range(0, 60, 3): # Começa no 0 e vai até 60 pulando de 3 em 3
        h_sinal = (ref + timedelta(minutes=minuto)).strftime("%H:%M")
        st.session_state.mem["espelho"].append(f"⏰ {h_sinal} | {c_esp}")

# Exibição em colunas para não ficar uma tripa gigante
if st.session_state.mem["espelho"]:
    cols = st.columns(4)
    for i, sinal in enumerate(st.session_state.mem["espelho"]):
        with cols[i % 4]:
            st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- TÓPICO 2: PEDRA ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎲 2. CÁLCULO POR PEDRA")
p_v = st.number_input("Número da Pedra:", 0, 14, 7, key="pedra_input")
if st.button("🚀 CALCULAR"):
    m_c = (p_v + datetime.now(fuso_ms).minute) % 60
    st.session_state.mem["pedra"] = [f"⏰ Minuto :{m_c:02d} | ENTRAR"]
for sinal in st.session_state.mem["pedra"]:
    st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- TÓPICO 3: PADRÃO 4-2-3 ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 3. PADRÃO 4-2-3")
c_ini = st.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="cor_423")
if st.button("🚀 GERAR 4-2-3"):
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms)
    st.session_state.mem["padrao_423"] = []
    c_at = c_ini
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.mem["padrao_423"].append(f"⏰ {ref_b.strftime('%H:%M')} | {c_at}")
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"
for sinal in st.session_state.mem["padrao_423"]:
    st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
