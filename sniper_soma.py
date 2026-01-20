import streamlit as st
import requests
import time

st.set_page_config(page_title="SOMA PRO", layout="wide")
st.markdown("<style>.stApp { background-color: #050505; color: white; }</style>", unsafe_allow_html=True)
st.title("🏹 ALGORITMO SOMA PRO")

area_sinal = st.empty()

def pegar_dados():
    # URL alternativa e mais estável
    url = "https://blaze.bet.br/api/roulette_games/recent"
    
    # Cabeçalho que imita um computador real para não ser bloqueado
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Referer": "https://blaze.bet.br/pt/games/double"
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        return None
    except:
        return None

while True:
    dados = pegar_dados()
    
    if dados and len(dados) > 0:
        ultima_cor = dados[0]['color']
        cor_nome = "BRANCO ⚪" if ultima_cor == 0 else ("VERMELHO 🔴" if ultima_cor == 1 else "PRETO ⚫")
        
        with area_sinal.container():
            st.success(f"✅ CONECTADO! Última cor: {cor_nome}")
            # Aqui você pode colocar o restante da sua lógica de sinal
    else:
        area_sinal.error("🚨 A Blaze bloqueou a conexão. Reinicie o App no menu lateral (Reboot).")
    
    time.sleep(12) # Espera um pouco mais para não parecer ataque
