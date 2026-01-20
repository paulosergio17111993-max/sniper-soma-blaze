import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO VISUAL RAIZ ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical (Como era antes: sem bolinhas) */
    .item-lista {
        padding: 12px; border-radius: 4px; margin-bottom: 6px;
        text-align: center; font-weight: bold; font-size: 16px;
        text-transform: uppercase;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 8px #fff; }
    .cor-1 { background-color: #f12c4c; color: #fff; }
    .cor-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Coluna de Terminais (Horários dos Brancos) */
    .card-brancos {
        background: #111; border-left: 5px solid #00ff00;
        padding: 15px; margin-bottom: 10px; border-radius: 0 5px 5px 0;
    }
    
    /* Painel de Sinal Central */
    .bloco-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 10px; padding: 40px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

# Estrutura de 3 Colunas idêntica à que você usava antes
col_hist, col_aviso, col_term = st.columns([1, 1.5, 1])

with col_hist:
    st.subheader("🕒 LISTA CORES")
    area_lista = st.empty()

with col_aviso:
    st.subheader("🎯 SINAL")
    area_sinal = st.empty()

with col_term:
    st.subheader("⚪ TERMINAIS")
    area_brancos = st.empty()

# --- CONEXÃO ESTÁVEL (BLAZE API) ---
URL = "https://blaze.bet.br/api/singleplayer-originals/originals/roulette_games/recent/1"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept": "application/json"
}

# Memória para os horários dos brancos
if 'historico_brancos' not in st.session_state:
    st.session_state.historico_brancos = []

while True:
    try:
        # Criando uma sessão para evitar o erro de bloqueio/reconexão
        with requests.Session() as s:
            r = s.get(URL, headers=HEADERS, timeout=10)
            dados = r.json()
        
        if dados:
            # 1. ATUALIZA LISTA DE CORES (Esquerda)
            with area_lista.container():
                for d in dados[:10]:
                    c = d['color']
                    n = d['roll']
                    nome = "BRANCO" if c == 0 else ("VERMELHO" if c == 1 else "PRETO")
                    st.markdown(f'<div class="item-lista cor-{c}">{nome} ({n})</div>', unsafe_allow_html=True)

            # 2. ATUALIZA SINAL (Centro)
            ultima = dados[0]['color']
            cor_entrada = "PRETO ⚫" if ultima == 1 else "VERMELHO 🔴"
            if ultima == 0: cor_entrada = "AGUARDAR..."
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="bloco-sinal">
                        <h2 style="color: #00ff00;">ENTRADA CONFIRMADA</h2>
                        <div style="font-size: 45px; font-weight: bold; margin: 20px 0;">{cor_entrada}</div>
                        <p style="background: white; color: black; padding: 5px; font-weight: bold; display: inline-block;">PROTEGER NO BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. ATUALIZA TERMINAIS (Direita - Horários)
            if dados[0]['color'] == 0:
                agora = datetime.now().strftime("%H:%M")
                if not st.session_state.historico_brancos or st.session_state.historico_brancos[0] != agora:
                    st.session_state.historico_brancos.insert(0, agora)

            with area_brancos.container():
                if not st.session_state.historico_brancos:
                    st.write("Aguardando branco...")
                for h in st.session_state.historico_brancos[:8]:
                    st.markdown(f"""
                        <div class="card-brancos">
                            <span style="color: #666; font-size: 12px;">HORÁRIO VICIADO</span><br>
                            <b style="font-size: 24px;">{h}</b>
                        </div>
                    """, unsafe_allow_html=True)
                    
    except Exception as e:
        area_sinal.warning("Sincronizando com a mesa... Aguarde alguns segundos.")
    
    time.sleep(10) # Intervalo maior para o Streamlit não bloquear a conexão
