import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE DESIGN PROFISSIONAL ---
st.set_page_config(page_title="SNIPER LIVE SCAN", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Barra de Histórico Horizontal */
    .historico-container {
        display: flex;
        flex-direction: row;
        background-color: #111;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 20px;
        overflow-x: hidden;
    }

    .bola {
        min-width: 32px; height: 32px; border-radius: 4px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 13px; color: white; margin-right: 8px;
    }

    /* Cores das Pedras */
    .cor-black { background-color: #2b2b2b; border: 1px solid #444; }
    .cor-red { background-color: #f12c4c; }
    .cor-white { background-color: #ffffff; color: #000; }
    
    .card-sinal {
        background: #0d0d0d; border: 2px solid #00ff00;
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0px 0px 15px rgba(0, 255, 0, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")
st.write("● MONITORANDO RODADAS AO VIVO...")

# Espaços que atualizam em tempo real
container_historico = st.empty()
container_sinal = st.empty()

# --- LOOP DE VARREDURA DA API ---
while True:
    try:
        # 1. Puxa os dados da API (Substitua pela sua URL real)
        # url = "URL_DA_SUA_PLATAFORMA"
        # r = requests.get(url)
        # dados = r.json()
        
        # Simulação de rodadas para teste:
        dados = [
            {"value": 10, "color": "black", "time": datetime.now()}, # Supondo que saiu o 10 agora
            {"value": 4, "color": "red"},
            {"value": 12, "color": "black"},
            {"value": 0, "color": "white"}
        ]

        # 2. Mostra o histórico na tela (as bolinhas passando)
        with container_historico.container():
            html_hist = '<div class="historico-container">'
            for p in dados[:14]:
                cor = f"cor-{p['color']}"
                html_hist += f'<div class="bola {cor}">{p["value"]}</div>'
            html_hist += '</div>'
            st.markdown(html_hist, unsafe_allow_html=True)

        # 3. Lógica: Se a última pedra for 10, calcula Minuto + 10
        ultima_rodada = dados[0]
        
        if ultima_rodada['value'] == 10:
            # Pega o minuto da hora que a pedra saiu
            minuto_saida = datetime.now().minute
            minuto_alvo = (minuto_saida + 10) % 60
            
            with container_sinal.container():
                st.markdown(f"""
                    <div class="card-sinal">
                        <h2 style="color: #00ff00; margin:0;">🎯 GATILHO DETECTADO!</h2>
                        <p style="color: #ccc;">A Pedra 10 saiu no minuto <b>{minuto_saida:02d}</b></p>
                        <hr style="border: 0.5px solid #333;">
                        <p style="font-size: 18px; margin:0;">ENTRADA NO MINUTO:</p>
                        <h1 style="font-size: 80px; margin: 10px 0; color: white;">{minuto_alvo:02d}</h1>
                        <p style="font-size: 22px;">COR: <b>PRETO ⚫</b></p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            container_sinal.info("🔍 Analisando rodadas... Aguardando a Pedra 10.")

    except Exception as e:
        st.error(f"Erro ao ler API: {e}")

    # Intervalo de 3 segundos para ler a próxima rodada
    time.sleep(3)
