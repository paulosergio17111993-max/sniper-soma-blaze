import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL SOMA PRO ---
st.set_page_config(page_title="SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .caixa { padding: 15px; border-radius: 4px; margin-bottom: 8px; text-align: center; font-weight: bold; font-size: 18px; text-transform: uppercase; }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .c-1 { background-color: #f12c4c; color: #fff; }
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

col1, col2, col3 = st.columns([1, 2, 1])
area_lista = col1.empty()
area_sinal = col2.empty()
area_term = col3.empty()

if 'brancos' not in st.session_state:
    st.session_state.brancos = []

def pegar_dados():
    # Link da API que não trava
    url = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/history?amount=10"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X)"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        dados = r.json()
        # Garante que vai pegar a lista, seja direto ou dentro de 'records'
        return dados.get('records', dados) if isinstance(dados, dict) else dados
    except:
        return None

while True:
    lista = pegar_dados()
    
    # Verifica se a lista existe antes de tentar ler (evita o KeyError da sua foto)
    if lista and isinstance(lista, list) and len(lista) > 0:
        with area_lista.container():
            st.markdown("### 🕒 LISTA CORES")
            for d in lista[:10]:
                c = d.get('color', 0)
                txt = "BRANCO" if c == 0 else ("VERMELHO" if c == 1 else "PRETO")
                st.markdown(f'<div class="caixa c-{c}">{txt}</div>', unsafe_allow_html=True)

        ultima_cor = lista[0].get('color', 0)
        sugestao = "PRETO ⚫" if ultima_cor == 1 else "VERMELHO 🔴"
        
        with area_sinal.container():
            st.markdown(f"""
                <div style="border:3px solid #00ff00; padding:40px; text-align:center; border-radius:15px; background: black;">
                    <h1 style="color:#00ff00;">SINAL CONFIRMADO</h1>
                    <div style="font-size:55px; font-weight:bold; margin:20px 0;">{sugestao}</div>
                    <p style="background:white; color:black; padding:10px; font-weight:bold; display:inline-block;">COBRIR BRANCO ⚪</p>
                </div>
            """, unsafe_allow_html=True)

        if ultima_cor == 0:
            h = datetime.now().strftime("%H:%M")
            if not st.session_state.brancos or st.session_state.brancos[0] != h:
                st.session_state.brancos.insert(0, h)
        
        with area_term.container():
            st.markdown("### ⚪ TERMINAIS")
            for b in st.session_state.brancos[:5]:
                st.success(f"BRANCO ÀS: {b}")
    else:
        area_sinal.warning("Conectando à mesa da Blaze... Aguarde o próximo giro.")

    time.sleep(10)
