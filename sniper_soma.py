import streamlit as st
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE LAYOUT (PRESERVA O QUE VOCÊ JÁ TEM) ---
st.set_page_config(page_title="SNIPER MS PRO", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #050505; color: white; }
    .box-estratégia { 
        padding: 20px; border-radius: 15px; border: 2px solid #6b46c1; 
        background-color: #0d0d0d; margin-bottom: 20px;
    }
    .alerta-preto { 
        background-color: #1a1a1a; color: white; border: 2px solid #ffffff; 
        padding: 15px; border-radius: 10px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO v6.0")

# --- 1. NOVO MÓDULO: ESTRATÉGIA SOMA 10 (SÓ ADICIONEI ESTE) ---
st.markdown('<div class="box-estratégia">', unsafe_allow_html=True)
st.subheader("➕ CÁLCULO SOMA 10 (ALVO PRETO)")
st.write("Identificou o 10 no histórico? Clique abaixo:")

if st.button("🎰 SAIU A PEDRA 10!"):
    minuto_agora = datetime.now().minute
    minuto_alvo = (minuto_agora + 10) % 60
    
    st.markdown(f"""
        <div class="alerta-preto">
            🎯 <b>GATILHO CONFIRMADO</b> <br>
            Soma: {minuto_agora} + 10 = {minuto_alvo:02d} <br>
            🚀 ENTRADA NO MINUTO: <b>{minuto_alvo:02d}</b> <br>
            <b>COR: PRETO ⚫</b>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- 2. SEU MÓDULO DA PEDRA 14 (NÃO MEXI EM NADA) ---
st.markdown('<div class="box-estratégia">', unsafe_allow_html=True)
st.subheader("🎯 MONITOR 14 (SEQUÊNCIA)")
if st.button("🔥 SAIU O 14! INICIAR CONTAGEM"):
    progresso = st.progress(0)
    for i in range(1, 8):
        st.write(f"Monitorando casa {i}...")
        progresso.progress(i * 14)
        time.sleep(1) 
        if i == 7:
            st.error("🚨 ENTRAR AGORA: VERMELHO 🔴")
st.markdown('</div>', unsafe_allow_html=True)


# --- 3. SUA LISTA DE BRANCOS SURREAL (NÃO MEXI EM NADA) ---
st.markdown('<div class="box-estratégia">', unsafe_allow_html=True)
st.subheader("⚪ LISTA DE BRANCOS (TERMINAIS)")
hora_operacao = st.number_input("HORA:", 0, 23, datetime.now().hour)

if st.button("🎯 GERAR TERMINAIS"):
    # Mantive seus terminais que estão moendo de acerto
    terminais = [0, 2, 3, 5, 9, 14, 15, 23, 24, 33, 35, 44, 51, 54, 56]
    st.write(f"Terminais viciados para {hora_operacao:02d}h:")
    col1, col2, col3 = st.columns(3)
    for idx, t in enumerate(terminais):
        with [col1, col2, col3][idx % 3]:
            st.success(f"{hora_operacao:02d}:{t:02d}")
st.markdown('</div>', unsafe_allow_html=True)

st.caption("Sniper MS PRO - Suas ferramentas estão todas aqui.")
