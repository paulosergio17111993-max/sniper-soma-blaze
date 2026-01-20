import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE INTERFACE ELITE ---
st.set_page_config(page_title="SNIPER API LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .historico-real {
        display: flex;
        flex-direction: row;
        background: #111;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #333;
        margin-bottom: 20px;
        overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 4px; font-weight: bold; color: white;
    }
    .cor-preto { background-color: #222; border: 1px solid #444; }
    .cor-vermelho { background-color: #d32f2f; }
    .cor-branco { background-color: #fff; color: #000; }
    
    .painel-sinal {
        background: #0d0d0d; border: 2px solid #6b46c1;
        border-radius: 15px; padding: 25px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - API CONNECT")

# --- CONEXÃO COM A API DA PLATAFORMA ---
def puxar_dados_api():
    try:
        # AQUI VOCÊ COLA O LINK DA API DA SUA PLATAFORMA
        url = "URL_DA_API_AQUI" 
        response = requests.get(url, timeout=5)
        return response.json() # Retorna a lista de pedras do site
    except:
        # Se a API falhar, ele retorna vazio para não travar o site
        return []

# --- LOOP DE ATUALIZAÇÃO AO VIVO ---
monitor = st.empty()

while True:
    with monitor.container():
        # 1. Busca os dados direto na fonte
        dados = puxar_dados_api()
        
        if dados:
            # Mostra o histórico igual ao site
            html_hist = '<div class="historico-real">'
            for p in dados[:15]: # Mostra as últimas 15 pedras
                cor = "cor-preto" if p['color'] == 'black' else "cor-vermelho" if p['color'] == 'red' else "cor-branco"
                html_hist += f'<div class="bola {cor}">{p["value"]}</div>'
            html_hist += '</div>'
            st.markdown(html_hist, unsafe_allow_html=True)
            
            # 2. Lógica Automática da Pedra 10
            ultima_pedra = dados[0] # A pedra que acabou de sair agora
            
            if ultima_pedra['value'] == 10:
                min_agora = datetime.now().minute
                min_alvo = (min_agora + 10) % 60
                
                st.markdown(f"""
                    <div class="painel-sinal">
                        <h2 style="color: #00ff00;">🎯 ENTRADA DETECTADA VIA API</h2>
                        <p>Gatilho: Pedra 10 às {datetime.now().strftime('%H:%M:%S')}</p>
                        <h1 style="font-size: 70px; color: white;">{min_alvo:02d}</h1>
                        <p style="font-size: 20px;">COR: <b>PRETO ⚫</b></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write("🔍 Monitorando API... Aguardando Pedra 10.")
        else:
            st.warning("Aguardando conexão com a API da plataforma...")

    # O Sniper checa a API a cada 3 segundos (tempo ideal para não ser bloqueado)
    time.sleep(3)
