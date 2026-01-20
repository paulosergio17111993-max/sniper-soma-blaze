import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE DESIGN (CLONE DA SMASH) ---
st.set_page_config(page_title="SNIPER SMASH LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-wrapper {
        display: flex; flex-direction: row; background-color: #111;
        padding: 12px; border-radius: 8px; border: 1px solid #333;
        margin-bottom: 25px; overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 14px; color: white; margin-right: 8px;
    }
    /* Mapeamento de Cores da API Smash */
    .cor-1 { background-color: #f12c4c; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .card-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 15px; padding: 30px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - LIVE")

# --- MOTOR DE CONEXÃO COM A API QUE VOCÊ PASSOU ---
def puxar_api_real():
    try:
        # Link da API da Smash/Plataforma
        url = "https://api.smashup.com/api/v1/games/double/history"
        headers = {'User-Agent': 'Mozilla/5.0'} # Para o site não bloquear o robô
        r = requests.get(url, headers=headers, timeout=5)
        return r.json()
    except:
        return []

# --- ÁREAS DE ATUALIZAÇÃO ---
container_hist = st.empty()
container_sinal = st.empty()

while True:
    dados = puxar_api_real()
    
    if dados:
        # 1. MOSTRA O HISTÓRICO EM TEMPO REAL
        with container_hist.container():
            st.write("🕒 RODADAS AO VIVO (SMASH):")
            html_hist = '<div class="historico-wrapper">'
            for p in dados[:15]: # Mostra as últimas 15 pedras
                html_hist += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
            html_hist += '</div>'
            st.markdown(html_hist, unsafe_allow_html=True)

        # 2. LÓGICA DA SOMA 10 (BUSCA NO HISTÓRICO)
        encontrou_10 = False
        for item in dados:
            if item['roll'] == 10:
                # Pega o minuto do 'created_at' do JSON: "2026-01-20T00:06:02.610Z"
                # O minuto são os caracteres na posição 14 e 15
                minuto_pedra = int(item['created_at'][14:16])
                minuto_alvo = (minuto_pedra + 10) % 60
                
                with container_sinal.container():
                    st.markdown(f"""
                        <div class="card-sinal">
                            <p style="color: #00ff00; font-weight: bold; margin:0;">🎯 SINAL AUTOMÁTICO DETECTADO</p>
                            <p style="color: #888; font-size: 14px;">Pedra 10 identificada no minuto {minuto_pedra:02d}</p>
                            <h1 style="font-size: 85px; margin: 10px 0; color: white;">{minuto_alvo:02d}</h1>
                            <p style="font-size: 24px;">ENTRADA: <b>PRETO ⚫</b></p>
                            <p style="color: #6b46c1; font-weight: bold;">CÁLCULO: {minuto_pedra} + 10 = {minuto_alvo:02d}</p>
                        </div>
                    """, unsafe_allow_html=True)
                encontrou_10 = True
                break 
        
        if not encontrou_10:
            container_sinal.info("🔍 Analisando API... Aguardando a Pedra 10 sair no histórico.")

    time.sleep(3) # Checa a API a cada 3 segundos
