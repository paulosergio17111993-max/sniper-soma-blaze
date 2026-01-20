import streamlit as st
import requests
import time
from datetime import datetime

st.set_page_config(page_title="SNIPER MS PRO", layout="centered")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .painel {
        background: #0a0a0a; border: 2px solid #00ff00;
        border-radius: 20px; padding: 40px; text-align: center;
    }
    .numero-alvo { font-size: 100px; font-weight: bold; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 SNIPER MS PRO")
placeholder = st.empty()

URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        r = requests.get(URL_API, timeout=5)
        dados = r.json().get('records', [])
        
        if dados:
            # Pega a pedra MAIS RECENTE (a primeira da lista)
            ultima_pedra = dados[0]
            minuto_agora = datetime.now().minute
            
            # Procura se existe um 10 nas últimas 3 rodadas para não ficar sinal velho
            pedra_10 = next((item for item in dados[:3] if item['roll'] == 10), None)
            
            with placeholder.container():
                if pedra_10:
                    minuto_pedra = int(pedra_10['created_at'][14:16])
                    minuto_alvo = (minuto_pedra + 10) % 60
                    
                    # SÓ MOSTRA O SINAL SE O MINUTO AINDA NÃO PASSOU
                    if minuto_agora <= minuto_alvo or (minuto_agora > 50 and minuto_alvo < 10):
                        st.markdown(f"""
                            <div class="painel">
                                <h2 style="color: #00ff00;">● SINAL ATIVO</h2>
                                <p>Pedra 10 detectada no minuto {minuto_pedra:02d}</p>
                                <div class="numero-alvo">{minuto_alvo:02d}</div>
                                <p style="font-size: 24px;">ENTRADA: <b>PRETO ⚫</b></p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("⌛ Sinal expirado. Aguardando próxima Pedra 10...")
                else:
                    st.warning("🔍 Monitorando... Nenhuma Pedra 10 recente no histórico.")
                    
    except:
        st.error("Erro ao conectar. Tentando novamente...")

    time.sleep(5) # Espera 5 segundos para checar de novo

