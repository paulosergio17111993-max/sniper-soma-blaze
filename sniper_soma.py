import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - FULL", layout="wide")

# --- ESTILO GERAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background: #161b22; border-radius: 12px; padding: 15px; 
        margin-bottom: 10px; border-left: 10px solid #00ff88;
    }
    .metric-box {
        background: #0d1117; padding: 15px; border-radius: 10px; border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}

# --- FUNÇÕES DE CÁLCULO ---
def gerar_423(h, m, cor):
    ref = datetime.now(fuso_ms).replace(hour=h, minute=m, second=0)
    pulos = [0, 4, 2, 3, 4, 2]
    lista = []
    c_at = cor
    for p in pulos:
        ref += timedelta(minutes=p)
        lista.append({"h": ref.strftime("%H:%M"), "c": c_at})
        c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"
    return lista

def gerar_3912(cor_zero):
    ref = datetime.now(fuso_ms).replace(minute=0, second=0)
    if datetime.now(fuso_ms).minute > 15: ref += timedelta(hours=1)
    lista = []
    for m in [3, 9, 12]:
        h_sinal = ref + timedelta(minutes=m)
        lista.append({"h": h_sinal.strftime("%H:%M"), "c": cor_zero})
    return lista

# --- LAYOUT PRINCIPAL ---
st.title("🏹 SNIPER MS - CENTRAL DE OPERAÇÕES")

# Sidebar com o Contador (Fica visível o tempo todo)
with st.sidebar:
    st.header("📊 PLACAR SG")
    c1, c2 = st.columns(2)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("LOSS", st.session_state.placar["LOSS"])
    
    if st.button("✅ REGISTRAR SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("❌ REGISTRAR LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()
    if st.button("🔄 ZERAR"): st.session_state.placar = {"SG": 0, "LOSS": 0}; st.rerun()

# Divisão por Abas para não tirar nada
tab1, tab2, tab3 = st.tabs(["💎 PADRÃO ESPELHO (3-9-12)", "🎲 CÁLCULO POR PEDRA", "🎯 PADRÃO 4-2-3"])

with tab1:
    st.subheader("Estratégia Repetição Minuto :00")
    c_zero = st.selectbox("Cor que saiu no :00:", ["VERMELHO 🔴", "PRETO ⚫"], key="zero")
    if st.button("🚀 GERAR ESPELHO"):
        st.session_state.res_espelho = gerar_3912(c_zero)
    
    if 'res_espelho' in st.session_state:
        for s in st.session_state.res_espelho:
            cor_b = "#ff4b4b" if "🔴" in s['c'] else "#fff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_b}">⏰ {s["h"]} | {s["c"]} (SG)</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("Cálculo: Minuto + Pedra")
    pedra = st.number_input("Pedra que saiu:", 0, 14, 7)
    min_r = st.number_input("Minuto do Relógio:", 0, 59, datetime.now(fuso_ms).minute)
    m_final = (pedra + min_r) % 60
    st.info(f"O primeiro sinal será no minuto: {m_final}")
    # Aqui pode chamar qualquer gerador usando o m_final

with tab3:
    st.subheader("Padrão Sequencial 4-2-3-4-2")
    col_a, col_b = st.columns(2)
    h_423 = col_a.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
    m_423 = col_b.number_input("Minuto:", 0, 59, datetime.now(fuso_ms).minute)
    cor_423 = st.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"], key="c423")
    
    if st.button("🚀 GERAR SEQUÊNCIA 4-2-3"):
        st.session_state.res_423 = gerar_423(h_423, m_423, cor_423)
    
    if 'res_423' in st.session_state:
        for s in st.session_state.res_423:
            cor_b = "#ff4b4b" if "🔴" in s['c'] else "#fff"
            st.markdown(f'<div class="card-sinal" style="border-left-color:{cor_b}">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
