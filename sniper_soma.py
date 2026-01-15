import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL (CONFORME FOTOS) ---
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
    /* Botão Roxo das Fotos */
    .stButton>button { 
        background-color: #6a5acd; color: white; font-weight: bold; 
        width: 100%; height: 3.5em; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'mem' not in st.session_state:
    st.session_state.mem = {"espelho": [], "soma": [], "padrao_423": []}
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- BARRA LATERAL (PLACAR) ---
with st.sidebar:
    st.header("📊 PLACAR SG")
    st.metric("SG", st.session_state.placar["SG"])
    st.metric("LOSS", st.session_state.placar["LOSS"])
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()

st.title("🎯 SNIPER MS - CENTRAL DE OPERAÇÕES")

# --- 1. PADRÃO ESPELHO ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO ESPELHO (3-9-12)")
c_esp = st.selectbox("Cor que saiu no :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="esp_c")
if st.button("🚀 GERAR LISTA", key="btn_esp"):
    ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
    st.session_state.mem["espelho"] = []
    for p in [3, 9, 12]:
        h_s = (ref + timedelta(minutes=p)).strftime("%H:%M")
        st.session_state.mem["espelho"].append(f"⏰ {h_s} | {c_esp}")
for s in st.session_state.mem["espelho"]:
    st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. CÁLCULO POR PEDRA (FUNÇÃO SOMA) ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎲 2. CÁLCULO POR PEDRA (FUNÇÃO SOMA)")
p_val = st.number_input("Número da Pedra (0-14):", 0, 14, 7, key="pedra_n")
if st.button("🚀 GERAR LISTA", key="btn_soma"):
    # Lógica de Soma: Pedra + Minuto Atual
    minuto_atual = datetime.now(fuso_ms).minute
    resultado_soma = (p_val + minuto_atual) % 60
    st.session_state.mem["soma"] = [f"⏰ Minuto :{resultado_soma:02d} | ENTRAR NA COR DO :00"]

for s in st.session_state.mem["soma"]:
    st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. PADRÃO 4-2-3 ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 3. PADRÃO 4-2-3")
col1, col2, col3 = st.columns(3)
h_423 = col1.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
m_423 = col2.number_input("Minuto:", 0, 59, 10)
c_423 = col3.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"])

if st.button("🚀 GERAR LISTA", key="btn_423"):
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h_423), minute=int(m_423), second=0, microsecond=0)
    st.session_state.mem["padrao_423"] = []
    cor_at = c_423
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.mem["padrao_423"].append(f"⏰ {ref_b.strftime('%H:%M')} | {cor_at}")
        cor_at = "PRETO ⚫" if cor_at == "VERMELHO 🔴" else "VERMELHO 🔴"

if st.session_state.mem["padrao_423"]:
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.mem["padrao_423"]):
        with cols[i % 3]: st.markdown(f'<div class="card-sinal">{s}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
