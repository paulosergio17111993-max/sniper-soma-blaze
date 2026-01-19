import streamlit as st
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE DESIGN (TOTAL BLACK & PURPLE) ---
st.set_page_config(page_title="SNIPER LIVE HISTORY", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    
    /* Estilo das Bolinhas do Histórico */
    .bola {
        display: inline-block;
        width: 35px;
        height: 35px;
        border-radius: 50%;
        text-align: center;
        line-height: 35px;
        font-weight: bold;
        margin: 5px;
        color: white;
        border: 1px solid #333;
    }
    .preto { background-color: #1a1a1a; border: 1px solid #444; }
    .vermelho { background-color: #e02424; }
    .branco { background-color: #ffffff; color: #000; }
    
    .container-historico {
        background-color: #0d0d0d;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #6b46c1;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .card-sinal {
        background-color: #0d0d0d;
        border: 2px solid #00ff00;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - LIVE SCAN")

# --- SIMULAÇÃO DO HISTÓRICO EM TEMPO REAL ---
# Aqui o Sniper lê as últimas 10 pedras da plataforma
historico_fake = [
    {"v": 10, "c": "preto"}, {"v": 2, "c": "vermelho"}, {"v": 0, "c": "branco"},
    {"v": 14, "c": "vermelho"}, {"v": 8, "c": "preto"}, {"v": 7, "c": "vermelho"},
    {"v": 10, "c": "preto"}, {"v": 12, "c": "preto"}, {"v": 1, "c": "vermelho"}
]

# --- ÁREA DO HISTÓRICO AO VIVO ---
st.write("🕒 ÚLTIMAS RODADAS:")
html_historico = '<div class="container-historico">'
for p in historico_fake:
    classe = p['c']
    html_historico += f'<div class="bola {classe}">{p["v"]}</div>'
html_historico += '</div>'
st.markdown(html_historico, unsafe_allow_html=True)

# --- LÓGICA DE IDENTIFICAÇÃO ---
# O Sniper varre o histórico acima e procura o 10
ultima_pedra = historico_fake[0] # A mais recente

if ultima_pedra["v"] == 10:
    min_atual = datetime.now().minute
    min_alvo = (min_atual + 10) % 60
    
    st.markdown(f"""
        <div class="card-sinal">
            <p style="color: #00ff00; font-weight: bold;">● GATILHO IDENTIFICADO NO HISTÓRICO</p>
            <h1 style="font-size: 50px; color: white; margin: 0;">{min_alvo:02d}</h1>
            <p style="font-size: 20px; color: white;">ENTRADA: <b>PRETO ⚫</b></p>
            <small style="color: #666;">Baseado na Pedra 10 que acabou de sair</small>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("🔍 Monitorando rodadas... Aguardando Pedra 10 aparecer no topo.")

# Auto-refresh para simular o "Ao Vivo"
time.sleep(5)
st.rerun()
