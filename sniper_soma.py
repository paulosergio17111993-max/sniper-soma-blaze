import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="SNIPER MS PRO - LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-track {
        display: flex; background: #111; padding: 10px;
        border-radius: 8px; border: 1px solid #333; overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 4px; font-weight: bold;
    }
    .cor-1 { background-color: #f12c4c; color: white; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .alerta-soma {
        background: #0d0d0d; border: 2px solid #00ff00;
        border-radius: 15px; padding: 30px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - AO VIVO")

# --- CONECTOR REAL ---
def buscar_dados():
    try:
        # ⚠️ PAULO, COLOQUE O LINK DA API ENTRE AS ASPAS ABAIXO:
        url = "URL_DA_SUA_API_AQUI" 
        r = requests.get(url, timeout=5)
        return r.json()
    except:
        return []

# --- MOTOR DE ATUALIZAÇÃO ---
monitor_hist = st.empty()
monitor_sinal = st.empty()

while True:
    dados = buscar_dados()
    
    if dados:
        # 1. Mostra o Histórico de Rodadas Normais
        with monitor_hist.container():
            st.write("🕒 RODADAS DA PLATAFORMA:")
            html = '<div class="historico-track">'
            for p in dados[:15]:
                html += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)

        # 2. Monitora a Pedra 10 para fazer a SOMA
        ultima = dados[0]
        if ultima['roll'] == 10:
            # Pega o minuto do 'created_at' do seu JSON
            # Ex: "2026-01-20T00:06:02.610Z" -> pega o minuto 06
            horario_raw = ultima['created_at'].split('T')[1] # pega 00:06:02...
            minuto_original = int(horario_raw.split(':')[1]) # pega o 06
            
            minuto_alvo = (minuto_original + 10) % 60
            
            with monitor_sinal.container():
                st.markdown(f"""
                    <div class="alerta-soma">
                        <p style="color: #00ff00; font-weight: bold;">● SINAL GERADO (SOMA 10)</p>
                        <p style="color: #666;">Pedra 10 detectada no minuto {minuto_original:02d}</p>
                        <h1 style="font-size: 80px; margin: 10px 0;">{minuto_alvo:02d}</h1>
                        <p style="font-size: 22px;">PRÓXIMA ENTRADA: <b>PRETO ⚫</b></p>
                        <p style="color: #6b46c1; font-weight: bold;">SOMA: {minuto_original} + 10</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            monitor_sinal.info("🔍 Monitorando... Aguardando Pedra 10 no histórico ao vivo.")
            
    time.sleep(2) # Ele checa o site a cada 2 segundos
