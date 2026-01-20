import streamlit as st
import requests
import time
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DE DESIGN SNIPER ---
st.set_page_config(page_title="SNIPER MS PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .historico-container {
        display: flex; flex-direction: row; background-color: #111;
        padding: 10px; border-radius: 8px; border: 1px solid #333;
        margin-bottom: 20px; overflow-x: auto;
    }
    .bola {
        min-width: 32px; height: 32px; border-radius: 4px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 13px; color: white; margin-right: 6px;
    }
    .cor-1 { background-color: #f12c4c; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .card-sinal {
        background: #0d0d0d; border: 2px solid #6b46c1;
        border-radius: 15px; padding: 25px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - LIVE SCAN")

# --- ESPAÇOS DE ATUALIZAÇÃO ---
area_hist = st.empty()
area_sinal = st.empty()

def obter_dados():
    try:
        # COLOQUE O LINK DA SUA API ABAIXO:
        url = "SUA_URL_DA_API_AQUI"
        response = requests.get(url, timeout=5)
        return response.json()
    except:
        return []

while True:
    dados = obter_dados()
    
    if dados:
        with area_hist.container():
            st.write("🕒 RODADAS AO VIVO:")
            html_hist = '<div class="historico-container">'
            for p in dados[:15]: # Mostra as últimas 15
                html_hist += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
            html_hist += '</div>'
            st.markdown(html_hist, unsafe_allow_html=True)

        # LÓGICA DA SOMA 10
        ultima_pedra = dados[0]
        
        with area_sinal.container():
            if ultima_pedra['roll'] == 10:
                # Extrai o minuto da criação da pedra (padrão ISO)
                horario_str = ultima_pedra['created_at'].replace('Z', '')
                horario_dt = datetime.fromisoformat(horario_str)
                
                minuto_original = horario_dt.minute
                minuto_alvo = (minuto_original + 10) % 60
                
                st.markdown(f"""
                    <div class="card-sinal">
                        <h2 style="color: #00ff00; margin:0;">🎯 GATILHO IDENTIFICADO</h2>
                        <p style="color: #aaa;">Pedra 10 saiu no minuto: {minuto_original:02d}</p>
                        <h1 style="font-size: 80px; color: white; margin: 10px 0;">{minuto_alvo:02d}</h1>
                        <p style="font-size: 22px;">ENTRADA: <b>PRETO ⚫</b></p>
                        <small style="color: #6b46c1;">Soma Automática: {minuto_original} + 10</small>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("🔍 Monitorando histórico... Aguardando sair a Pedra 10.")
    
    time.sleep(2) # Atualiza a cada 2 segundos
