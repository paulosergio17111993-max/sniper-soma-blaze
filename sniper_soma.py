import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL (QUADRADOS ORGANIZADOS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .topico-bloco {
        background-color: #0d1117;
        border: 2px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        border-top: 5px solid #6a5acd;
    }
    .card-sinal { 
        background-color: #161b22; 
        border-radius: 8px; 
        padding: 12px; 
        margin-top: 8px; 
        border-left: 5px solid #00ff88;
        font-weight: bold;
    }
    .stButton>button { background-color: #6a5acd; color: white; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- LIMPEZA E INICIALIZAÇÃO DE MEMÓRIA (EVITA KEYERROR) ---
if 'mem' not in st.session_state or "padrao_423" not in st.session_state.mem:
    st.session_state.mem = {"espelho": [], "pedra": [], "padrao_423": []}

if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- BARRA LATERAL (PLACAR) ---
with st.sidebar:
    st.header("📊 PLACAR")
    st.metric("SG", st.session_state.placar.get("SG", 0))
    st.metric("LOSS", st.session_state.placar.get("LOSS", 0))
    if st.button("✅ REGISTRAR SG"): 
        st.session_state.placar["SG"] += 1
        st.rerun()
    if st.button("❌ REGISTRAR LOSS"): 
        st.session_state.placar["LOSS"] += 1
        st.rerun()
    if st.button("🔄 RESETAR TUDO"):
        st.session_state.mem = {"espelho": [], "pedra": [], "padrao_423": []}
        st.session_state.placar = {"SG": 0, "LOSS": 0}
        st.rerun()

st.title("🎯 SNIPER MS - CENTRAL DE FERRAMENTAS")

# --- TÓPICO 1: ESPELHO ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("💎 1. PADRÃO ESPELHO (3-9-12)")
c_esp = st.selectbox("Cor no minuto :00:", ["PRETO ⚫", "VERMELHO 🔴"], key="t1")
if st.button("🚀 GERAR LISTA ESPELHO"):
    ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
    st.session_state.mem["espelho"] = []
    for p in [3, 9, 12]:
        h = (ref + timedelta(minutes=p)).strftime("%H:%M")
        st.session_state.mem["espelho"].append(f"⏰ {h} | {c_esp}")

for sinal in st.session_state.mem["espelho"]:
    st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- TÓPICO 2: PEDRA ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎲 2. CÁLCULO POR PEDRA")
col_p1, col_p2 = st.columns(2)
p_v = col_p1.number_input("Número da Pedra:", 0, 14, 7)
m_r = col_p2.number_input("Minuto do Relógio:", 0, 59, datetime.now(fuso_ms).minute)
if st.button("🚀 CALCULAR AGORA"):
    m_c = (p_v + m_r) % 60
    st.session_state.mem["pedra"] = [f"⏰ Minuto :{m_c:02d} | ENTRAR NA COR DO :00"]

for sinal in st.session_state.mem["pedra"]:
    st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- TÓPICO 3: PADRÃO 4-2-3 ---
st.markdown('<div class="topico-bloco">', unsafe_allow_html=True)
st.subheader("🎯 3. PADRÃO 4-2-3")
c1, c2, c3 = st.columns(3)
h_b = c1.number_input("Hora Inicial:", 0, 23, datetime.now(fuso_ms).hour)
m_b = c2.number_input("Minuto Inicial:", 0, 59, 10)
cor_b = c3.selectbox("Cor do Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="t3")

if st.button("🚀 GERAR SEQUÊNCIA 4-2-3"):
    pulos = [0, 4, 2, 3, 4, 2]
    ref_b = datetime.now(fuso_ms).replace(hour=int(h_b), minute=int(m_b), second=0, microsecond=0)
    st.session_state.mem["padrao_423"] = []
    c_at = cor_b
    for p in pulos:
        ref_b += timedelta(minutes=p)
        st.session_state.mem["padrao_423"].append(f"⏰ {ref_b.strftime('%H:%M')} | {c_at}")
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"

if st.session_state.mem["padrao_423"]:
    cols = st.columns(3)
    for i, sinal in enumerate(st.session_state.mem["padrao_423"]):
        with cols[i % 3]:
            st.markdown(f'<div class="card-sinal">{sinal}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
