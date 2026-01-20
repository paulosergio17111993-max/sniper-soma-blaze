import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL RAIZ ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .item-lista {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .cor-1 { background-color: #f12c4c; color: #fff; }
    .cor-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }
    
    .card-term {
        background: #111; border-left: 5px solid #00ff00;
        padding: 20px; margin-bottom: 12px;
    }
    .painel-sinal {
        background: #000; border: 3px solid #00ff00;
        border-radius: 15px; padding: 50px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

col1, col2, col3 = st.columns([1, 1.8, 1])

with col1:
    st.markdown("### 🕒 LISTA CORES")
    area_lista = st.empty()
with col2:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()
with col3:
    st.markdown("### ⚪ TERMINAIS")
    area_brancos = st.empty()

if 'brancos_viciados' not in st.session_state:
    st.session_state.brancos_viciados = []

# --- CONEXÃO DISFARÇADA ---
def pegar_dados():
    url = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
    except:
        return None

while True:
    dados = pegar_dados()
    
    if dados:
        # 1. LISTA (ESQUERDA)
        with area_lista.container():
            for d in dados[:10]:
                c = d['color']
                n = d['roll']
                txt = "BRANCO" if c == 0 else ("VERMELHO" if c == 1 else "PRETO")
                st.markdown(f'<div class="item-lista cor-{c}">{txt} ({n})</div>', unsafe_allow_html=True)

        # 2. SINAL (CENTRO)
        ultima = dados[0]['color']
        sinal = "PRETO ⚫" if ultima == 1 else "VERMELHO 🔴"
        if ultima == 0: sinal = "AGUARDAR..."
        
        with area_sinal.container():
            st.markdown(f"""
                <div class="painel-sinal">
                    <h1 style="color: #00ff00; margin:0;">SINAL CONFIRMADO</h1>
                    <div style="font-size: 50px; font-weight: bold; margin: 25px 0;">{sinal}</div>
                    <p style="background:white; color:black; padding:10px; font-weight:bold; display:inline-block; border-radius:5px;">COBRIR BRANCO ⚪</p>
                </div>
            """, unsafe_allow_html=True)

        # 3. TERMINAIS (DIREITA)
        if dados[0]['color'] == 0:
            hora = datetime.now().strftime("%H:%M")
            if not st.session_state.brancos_viciados or st.session_state.brancos_viciados[0] != hora:
                st.session_state.brancos_viciados.insert(0, hora)

        with area_brancos.container():
            for b in st.session_state.brancos_viciados[:8]:
                st.markdown(f'<div class="card-term"><small>BRANCO ÀS:</small><br><b style="font-size:25px;">{b}</b></div>', unsafe_allow_html=True)
    else:
        area_sinal.warning("Sincronizando... Se demorar, recarregue a página.")
    
    time.sleep(12)
