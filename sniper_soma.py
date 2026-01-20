import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL (SOMA PRO ORIGINAL) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista Vertical de Cores */
    .caixa-item {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
        text-transform: uppercase;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } /* Branco */
    .c-1 { background-color: #f12c4c; color: #fff; } /* Vermelho */
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; } /* Preto */

    /* Terminais (Horários) */
    .terminal-card {
        background: #111; border-left: 6px solid #f12c4c;
        padding: 20px; margin-bottom: 12px; border-radius: 4px;
    }
    
    /* Painel Central */
    .alerta-sinal {
        background: #000; border: 3px solid #f12c4c;
        border-radius: 15px; padding: 60px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO - BLAZE")

col_hist, col_sinal, col_term = st.columns([1, 1.8, 1])

with col_hist:
    st.markdown("### 🕒 HISTÓRICO")
    area_lista = st.empty()

with col_sinal:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()

with col_term:
    st.markdown("### ⚪ TERMINAIS")
    area_brancos = st.empty()

# URL DA API QUE ENCONTREI NOS TEUS FICHEIROS
URL_API = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"

# Memória para os terminais
if 'lista_brancos' not in st.session_state:
    st.session_state.lista_brancos = []

while True:
    try:
        # Puxa 20 resultados para ter histórico
        r = requests.get("https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent", timeout=10)
        dados = r.json()
        
        if dados:
            # 1. LISTA VERTICAL (Lado Esquerdo)
            with area_lista.container():
                for item in dados[:12]:
                    cor = item['color']
                    num = item['roll']
                    label = "BRANCO" if cor == 0 else ("VERMELHO" if cor == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-item c-{cor}">{label} ({num})</div>', unsafe_allow_html=True)

            # 2. SINAL (Centro)
            ultima_cor = dados[0]['color']
            sugestao = "PRETO ⚫" if ultima_cor == 1 else "VERMELHO 🔴"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-sinal">
                        <h1 style="color: white; margin:0;">SINAL DETECTADO</h1>
                        <div style="font-size: 55px; font-weight: bold; margin: 30px 0;">{sugestao}</div>
                        <p style="background: white; color: black; padding: 10px; font-weight: bold; display: inline-block;">COBRIR O BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS (Lado Direito)
            # Filtra os brancos que saíram agora e guarda o horário
            for item in dados[:5]:
                if item['color'] == 0:
                    hora_atual = datetime.now().strftime("%H:%M")
                    if hora_atual not in st.session_state.lista_brancos:
                        st.session_state.lista_brancos.insert(0, hora_atual)

            with area_brancos.container():
                for b in st.session_state.lista_brancos[:8]:
                    st.markdown(f"""
                        <div class="terminal-card">
                            <small style="color: #666;">BRANCO ÀS:</small><br>
                            <b style="font-size: 28px;">{b}</b>
                        </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        area_sinal.warning("A aguardar nova rodada da Blaze...")
    
    time.sleep(5)
