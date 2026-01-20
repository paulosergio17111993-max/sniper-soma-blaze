import streamlit as st
import time
from datetime import datetime

# --- DESIGN SNIPER MS PRO ---
st.set_page_config(page_title="SNIPER LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-real {
        display: flex; flex-direction: row; background: #111;
        padding: 10px; border-radius: 8px; border: 1px solid #333;
        margin-bottom: 20px; overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 4px; font-weight: bold;
    }
    .cor-1 { background-color: #f12c4c; color: white; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .alerta-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 15px; padding: 25px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - LIVE")

# --- SEUS DADOS REAIS (PARA O CÓDIGO FUNCIONAR AGORA) ---
dados_plataforma = [
    {"created_at":"2026-01-20T00:10:03Z","color":2,"roll":14},
    {"created_at":"2026-01-20T00:09:32Z","color":1,"roll":4},
    {"created_at":"2026-01-20T00:06:02Z","color":2,"roll":10}, # GATILHO 10 AQUI
    {"created_at":"2026-01-20T00:05:32Z","color":2,"roll":13}
]

# --- RENDERIZAÇÃO DO HISTÓRICO ---
st.write("🕒 HISTÓRICO REAL DETECTADO:")
html_hist = '<div class="historico-real">'
for p in dados_plataforma:
    html_hist += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
html_hist += '</div>'
st.markdown(html_hist, unsafe_allow_html=True)

# --- LÓGICA DA SOMA AUTOMÁTICA ---
# Vamos varrer o histórico. Quando achar o 10, ele faz a soma.
for rodada in dados_plataforma:
    if rodada['roll'] == 10:
        # Pega o minuto do "created_at" (Ex: 00:06:02 -> minuto 06)
        minuto_saida = int(rodada['created_at'][14:16]) 
        minuto_alvo = (minuto_saida + 10) % 60
        
        st.markdown(f"""
            <div class="alerta-sinal">
                <p style="color: #00ff00; font-weight: bold; margin:0;">🎯 SINAL DETECTADO NO HISTÓRICO</p>
                <p style="color: #666; font-size: 14px;">A Pedra 10 saiu no minuto {minuto_saida:02d}</p>
                <h1 style="font-size: 70px; margin: 10px 0; color: white;">{minuto_alvo:02d}</h1>
                <p style="font-size: 20px;">PRÓXIMA ENTRADA: <b>PRETO ⚫</b></p>
                <p style="color: #6b46c1; font-weight: bold;">SOMA: {minuto_saida} + 10 = {minuto_alvo:02d}</p>
            </div>
        """, unsafe_allow_html=True)
        break # Para na primeira pedra 10 que encontrar

st.info("🔍 Robô monitorando o histórico... Próxima atualização em breve.")
