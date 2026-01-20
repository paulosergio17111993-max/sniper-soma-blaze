import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO TELA CHEIA E CORES ---
st.set_page_config(page_title="SNIPER MS PRO", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    
    .painel-sinal {
        background: #0a0a0a;
        border: 3px solid #00ff00;
        border-radius: 20px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.15);
        margin-top: 20px;
    }
    
    .minuto-alvo {
        font-size: 120px;
        font-weight: bold;
        color: #ffffff;
        margin: 10px 0;
        line-height: 1;
    }
    
    .status-badge {
        background: #00ff00;
        color: black;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE LEITURA (API SMASH) ---
URL_API = "https://api.smashup.com/api/v1/games/double/history"

def monitorar():
    try:
        r = requests.get(URL_API, timeout=5)
        # Entra direto nos records que você mandou
        dados = r.json().get('records', [])
        return dados
    except:
        return None

# --- INTERFACE ---
st.title("🎯 SNIPER MS PRO")
placeholder = st.empty()

while True:
    dados = monitorar()
    
    if dados:
        # Busca o 10 mais recente
        pedra_10 = next((item for item in dados if item['roll'] == 10), None)
        
        with placeholder.container():
            if pedra_10:
                # Pega o minuto do seu JSON (ex: 23:28:58 -> 28)
                minuto_bruto = int(pedra_10['created_at'][14:16])
                minuto_alvo = (minuto_bruto + 10) % 60
                
                st.markdown(f"""
                    <div class="painel-sinal">
                        <span class="status-badge">● Sinal Identificado</span>
                        <p style="color: #888; margin-top: 20px;">PEDRA 10 SAIU NO MINUTO: {minuto_bruto:02d}</p>
                        <div style="color: #00ff00; font-size: 20px; font-weight: bold;">ENTRAR NO MINUTO:</div>
                        <div class="minuto-alvo">{minuto_alvo:02d}</div>
                        <div style="font-size: 30px; letter-spacing: 2px;">COR: <b>PRETO ⚫</b></div>
                        <hr style="border: 0.5px solid #222; margin: 25px 0;">
                        <p style="color: #6b46c1; font-weight: bold;">LÓGICA: SOMA 10 ATIVA</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="text-align: center; padding: 100px; color: #444;">
                        <h2>🔍 MONITORANDO...</h2>
                        <p>Aguardando sair uma Pedra 10 no histórico para calcular o alvo.</p>
                    </div>
                """, unsafe_allow_html=True)
                
    time.sleep(2) # Rápido para não perder o tempo da aposta
