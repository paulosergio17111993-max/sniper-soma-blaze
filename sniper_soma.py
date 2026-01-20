import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL (SOMA PRO ORIGINAL) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista Vertical de Cores (Estilo Blocos do Soma Pro) */
    .caixa-item {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
        text-transform: uppercase;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } /* BRANCO */
    .c-1 { background-color: #f12c4c; color: #fff; } /* VERMELHO */
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; } /* PRETO */

    /* Terminais (Horários na Direita) */
    .terminal-card {
        background: #111; border-left: 6px solid #f12c4c;
        padding: 20px; margin-bottom: 12px; border-radius: 4px;
    }
    
    /* Painel Central de Sinal */
    .alerta-sinal {
        background: #000; border: 3px solid #f12c4c;
        border-radius: 15px; padding: 60px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO - BLAZE")

# Layout de 3 Colunas: Histórico | Sinal | Terminais
col_hist, col_sinal, col_term = st.columns([1, 1.8, 1])

with col_hist:
    st.markdown("### 🕒 LISTA CORES")
    area_lista = st.empty()

with col_sinal:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()

with col_term:
    st.markdown("### ⚪ TERMINAIS")
    area_brancos = st.empty()

# URL DA API ENCONTRADA NOS SEUS ARQUIVOS (BLAZE)
URL_API = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"

# Memória para não perder os horários dos brancos na tela
if 'lista_brancos' not in st.session_state:
    st.session_state.lista_brancos = []

while True:
    try:
        # Puxa os resultados reais da Blaze
        r = requests.get(URL_API, timeout=10)
        dados = r.json()
        
        if dados:
            # 1. LISTA VERTICAL (Lado Esquerdo - Sem bolinhas)
            with area_lista.container():
                for item in dados[:12]:
                    cor = item['color']
                    num = item['roll']
                    label = "BRANCO" if cor == 0 else ("VERMELHO" if cor == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-item c-{cor}">{label} ({num})</div>', unsafe_allow_html=True)

            # 2. SINAL (Centro - Limpo e Direto)
            ultima_cor = dados[0]['color']
            # Lógica simples de inversão baseada nos seus scripts
            sugestao = "PRETO ⚫" if ultima_cor == 1 else "VERMELHO 🔴"
            if ultima_cor == 0: sugestao = "AGUARDAR..."
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-sinal">
                        <h1 style="color: white; margin:0;">SINAL DETECTADO</h1>
                        <div style="font-size: 55px; font-weight: bold; margin: 30px 0;">{sugestao}</div>
                        <p style="background: white; color: black; padding: 10px; font-weight: bold; display: inline-block; border-radius: 5px;">
                            COBRIR O BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS (Lado Direito - Pega o horário atual quando sai branco)
            if dados[0]['color'] == 0:
                hora_minuto = datetime.now().strftime("%H:%M")
                if not st.session_state.lista_brancos or st.session_state.lista_brancos[0] != hora_minuto:
                    st.session_state.lista_brancos.insert(0, hora_minuto)

            with area_brancos.container():
                if not st.session_state.lista_brancos:
                    st.write("Monitorando novos brancos...")
                for b in st.session_state.lista_brancos[:8]:
                    st.markdown(f"""
                        <div class="terminal-card">
                            <small style="color: #666;">BRANCO ÀS:</small><br>
                            <b style="font-size: 28px;">{b}</b>
                        </div>
                    """, unsafe_allow_html=True)

    except Exception:
        area_sinal.warning("Conectando à plataforma...")
    
    time.sleep(5)
