import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO E ESTILO RAIZ ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical */
    .item-cor {
        padding: 8px; border-radius: 4px; margin-bottom: 4px;
        font-weight: bold; text-align: center; font-size: 14px;
    }
    .c-0 { background-color: #ffffff; color: #000; } /* Branco */
    .c-1 { background-color: #f12c4c; color: #fff; } /* Vermelho */
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; } /* Preto */

    /* Terminais Viciados (Brancos) */
    .terminal-branco {
        background: #111; border-left: 5px solid #fff;
        padding: 12px; margin-bottom: 10px; border-radius: 0 8px 8px 0;
    }
    
    /* Painel de Sinal Inteligente */
    .painel-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 15px; padding: 40px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# URL DA API E CABEÇALHO
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {"User-Agent": "Mozilla/5.0"}

st.title("🏹 SNIPER MS PRO - OPERACIONAL")

# Criando as colunas conforme o seu layout antigo
col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    st.markdown("### 🎯 PRÓXIMA ENTRADA")
    area_sinal = st.empty()

with col2:
    st.markdown("### 🕒 LISTA DE CORES")
    area_cores = st.empty()

with col3:
    st.markdown("### ⚪ TERMINAIS (BRANCO)")
    area_brancos = st.empty()

while True:
    try:
        r = requests.get(URL_API, headers=HEADERS, timeout=10)
        dados = r.json().get('records', [])
        
        if dados:
            # --- FUNÇÃO 1: ANÁLISE DE SINAL ---
            ultima_cor = dados[0]['color']
            # Lógica de tendência: se repete muito uma cor, sugere a outra
            sinal = "VERMELHO 🔴" if ultima_cor == 2 else "PRETO ⚫"
            if ultima_cor == 0: sinal = "AGUARDAR ⏳"

            with area_sinal.container():
                st.markdown(f"""
                    <div class="painel-sinal">
                        <div style="color: #00ff00; letter-spacing: 2px; font-size: 12px;">ESTRATÉGIA ATIVA</div>
                        <div style="font-size: 40px; font-weight: bold; margin: 20px 0;">{sinal}</div>
                        <div style="background: white; color: black; padding: 5px 15px; display: inline-block; border-radius: 5px; font-weight: bold;">
                            PROTEGER NO BRANCO
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # --- FUNÇÃO 2: LISTA DE CORES VERTICAL ---
            with area_cores.container():
                for p in dados[:15]:
                    nome = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="item-cor c-{p["color"]}">{nome} ({p["roll"]})</div>', unsafe_allow_html=True)

            # --- FUNÇÃO 3: TERMINAIS VICIADOS (HORÁRIOS DO BRANCO) ---
            with area_brancos.container():
                brancos = [d for d in dados if d['color'] == 0]
                for b in brancos[:8]:
                    hora = b['created_at'][11:16]
                    st.markdown(f"""
                        <div class="terminal-branco">
                            <span style="color: #888; font-size: 11px;">TERMINAL CONFIRMADO</span><br>
                            <b style="font-size: 20px;">{hora}</b>
                        </div>
                    """, unsafe_allow_html=True)

    except:
        st.error("Reconectando às funções...")

    time.sleep(5)
