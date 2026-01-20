import streamlit as st
from datetime import datetime
import time

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="SNIPER MS PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-track {
        display: flex; background: #111; padding: 12px;
        border-radius: 8px; border: 1px solid #333; overflow-x: auto;
        margin-bottom: 20px;
    }
    .bola {
        min-width: 32px; height: 32px; border-radius: 4px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 4px; font-weight: bold; font-size: 13px;
    }
    .cor-1 { background-color: #f12c4c; color: white; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .card-sinal {
        background: #0d0d0d; border: 2px solid #6b46c1;
        border-radius: 15px; padding: 30px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - AO VIVO")

# --- SEUS DADOS REAIS (MAPEADOS) ---
dados_atuais = [
    {"roll": 14, "color": 2, "time": "00:10"},
    {"roll": 4, "color": 1, "time": "00:09"},
    {"roll": 10, "color": 2, "time": "00:06"}, # GATILHO IDENTIFICADO
    {"roll": 13, "color": 2, "time": "00:05"}
]

# 1. MOSTRA O HISTÓRICO CONFORME O SITE
st.write("🕒 HISTÓRICO DE RODADAS:")
html_feed = '<div class="historico-track">'
for p in dados_atuais:
    html_feed += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
html_feed += '</div>'
st.markdown(html_feed, unsafe_allow_html=True)

# 2. LÓGICA DE SOMA AUTOMÁTICA (Minuto + 10)
for rodada in dados_atuais:
    if rodada['roll'] == 10:
        minuto_saida = int(rodada['time'].split(':')[1])
        minuto_alvo = (minuto_saida + 10) % 60
        
        st.markdown(f"""
            <div class="card-sinal">
                <p style="color: #00ff00; font-weight: bold;">● GATILHO CONFIRMADO</p>
                <p style="color: #aaa; font-size: 14px;">Pedra 10 detectada às {rodada['time']}</p>
                <h1 style="font-size: 80px; margin: 15px 0; color: white;">{minuto_alvo:02d}</h1>
                <p style="font-size: 22px;">PRÓXIMA ENTRADA: <b>PRETO ⚫</b></p>
                <p style="color: #6b46c1; font-weight: bold;">SOMA: {minuto_saida} + 10</p>
            </div>
        """, unsafe_allow_html=True)
        break # Mostra apenas o sinal da pedra 10 mais recente

st.info("🔍 Monitorando rodadas... Aguardando próxima Pedra 10.")
