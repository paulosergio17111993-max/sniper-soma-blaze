import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER SOMA BLAZE", layout="centered")

# Estilização para deixar o fundo escuro e os cards bonitos
st.markdown("""
    <style>
    .main { background-color: #0b0e11; }
    div[data-testid="stMetricValue"] { color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #1a2026; color: white; border: 1px solid #333; }
    .stButton>button:hover { border-color: #f7b924; color: #f7b924; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DOS CONTADORES (A PLACA) ---
if 'sg' not in st.session_state:
    st.session_state.sg = 0
if 'g1' not in st.session_state:
    st.session_state.g1 = 0
if 'loss' not in st.session_state:
    st.session_state.loss = 0

# --- LÓGICA DE CÁLCULO ---
total_acertos = st.session_state.sg + st.session_state.g1

# --- EXIBIÇÃO DA PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"<div style='text-align: center; background: #1a2026; padding: 10px; border-radius: 5px; border-bottom: 4px solid #00ff88;'><b style='color: #00ff88;'>SG</b><br><span style='font-size: 25px;'>{st.session_state.sg}</span></div>", unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='text-align: center; background: #1a2026; padding: 10px; border-radius: 5px; border-bottom: 4px solid #00d4ff;'><b style='color: #00d4ff;'>G1</b><br><span style='font-size: 25px;'>{st.session_state.g1}</span></div>", unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='text-align: center; background: #1a2026; padding: 10px; border-radius: 5px; border-bottom: 4px solid #ff4d4d;'><b style='color: #ff4d4d;'>LOSS</b><br><span style='font-size: 25px;'>{st.session_state.loss}</span></div>", unsafe_allow_html=True)

with col4:
    st.markdown(f"<div style='text-align: center; background: #1a2026; padding: 10px; border-radius: 5px; border-bottom: 4px solid #f7b924;'><b style='color: #f7b924;'>TOTAL</b><br><span style='font-size: 25px;'>{total_acertos}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- ÁREA DO RADAR DE SINAIS ---
st.write("### 📋 RADAR DE SINAIS (LISTA)")

# Exemplo de como os sinais da sua lista vão aparecer
# Aqui você pode conectar a sua função de gerar lista
lista_exemplo = [
    {"hora": "20:10", "cor": "VERMELHO 🔴"},
    {"hora": "20:15", "cor": "PRETO ⚫"},
    {"hora": "20:22", "cor": "VERMELHO 🔴"},
]

for sinal in lista_exemplo:
    with st.container():
        c1, c2, c3, c4, c5 = st.columns([2, 3, 1, 1, 1])
        c1.write(f"⏰ **{sinal['hora']}**")
        c2.write(f"{sinal['cor']}")
        
        # Botões para você validar o sinal enquanto o robô processa
        if c3.button("SG", key=f"sg_{sinal['hora']}"):
            st.session_state.sg += 1
            st.rerun()
        if c4.button("G1", key=f"g1_{sinal['hora']}"):
            st.session_state.g1 += 1
            st.rerun()
        if c5.button("L", key=f"l_{sinal['hora']}"):
            st.session_state.loss += 1
            st.rerun()

# --- BOTÃO PARA LIMPAR TUDO ---
if st.sidebar.button("Zerar Placar"):
    st.session_state.sg = 0
    st.session_state.g1 = 0
    st.session_state.loss = 0
    st.rerun()
