import streamlit as st
import time
from datetime import datetime

# --- CONFIGURAÇÃO E ESTILO (BLINDADO) ---
st.set_page_config(page_title="SNIPER MS PRO v6.0", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .quadrado-sniper { 
        padding: 20px; border-radius: 12px; border: 2px solid #6b46c1; 
        background-color: #0d0d0d; margin-bottom: 20px;
    }
    .status-vivo { color: #00ff00; font-size: 12px; font-weight: bold; text-align: center; }
    .alerta-preto { background-color: #1a1a1a; border: 2px solid #ffffff; padding: 15px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO v6.0")

# --- 1. QUADRADO AO VIVO: SOMA 10 (PRETO) ---
st.markdown('<div class="quadrado-sniper">', unsafe_allow_html=True)
st.markdown('<p class="status-vivo">● MONITORANDO AO VIVO (ESTRATÉGIA SOMA 10)</p>', unsafe_allow_html=True)
st.subheader("➕ CALCULADORA AUTOMÁTICA")

# Simulador de Gatilho (No real, ele lê a API)
if st.checkbox("ATIVAR VIGIA DA PEDRA 10"):
    st.info("Buscando Pedra 10 no histórico ao vivo...")
    # Simulação de detecção
    pedra_fake = 10 
    if pedra_fake == 10:
        min_atual = datetime.now().minute
        min_alvo = (min_atual + 10) % 60
        st.markdown(f"""
            <div class="alerta-preto">
                🎯 GATILHO DETECTADO! <br>
                SOMA: {min_atual} + 10 = <b>{min_alvo:02d}</b> <br>
                ENTRADA NO MINUTO: <b>{min_alvo:02d} (PRETO ⚫)</b>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. QUADRADO DA PEDRA 14 (SEQUÊNCIA 7 CASAS) ---
st.markdown('<div class="quadrado-sniper">', unsafe_allow_html=True)
st.subheader("🎯 MONITOR 14 (SEQUÊNCIA)")
if st.button("🔥 SAIU O 14! MONITORAR 7 CASAS"):
    bar = st.progress(0)
    for i in range(1, 8):
        st.write(f"Monitorando casa {i}...")
        bar.progress(i * 14)
        time.sleep(0.5) # Rápido para teste
        if i == 7:
            st.error("🚨 ENTRAR AGORA: VERMELHO 🔴")
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. QUADRADO DOS BRANCOS (SEUS TERMINAIS VICIADOS) ---
st.markdown('<div class="quadrado-sniper">', unsafe_allow_html=True)
st.subheader("⚪ LISTA DE BRANCO (TERMINAIS)")
h_b = st.number_input("HORA:", 0, 23, datetime.now().hour)
if st.button("🎯 GERAR TERMINAIS"):
    terminais = [0, 2, 3, 5, 9, 14, 15, 23, 24, 33, 35, 44, 51, 54, 56]
    cols = st.columns(3)
    for idx, t in enumerate(terminais):
        with cols[idx % 3]:
            st.success(f"{h_b:02d}:{t:02d}")
st.markdown('</div>', unsafe_allow_html=True)
