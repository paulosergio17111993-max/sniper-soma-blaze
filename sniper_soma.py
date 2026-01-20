import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO VISUAL RAIZ (SOMA PRO) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical Estilo Antigo */
    .caixa-cor {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .c-1 { background-color: #f12c4c; color: #fff; }
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Terminais Viciados (Horários) */
    .card-terminal {
        background: #111; border-left: 6px solid #00ff00;
        padding: 20px; margin-bottom: 12px; border-radius: 0 10px 10px 0;
    }
    
    /* Painel Central */
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
    area_terminais = st.empty()

# --- CONEXÃO BLINDADA ---
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.smashup.com/"
}

while True:
    try:
        # Usa uma sessão para manter a conexão ativa
        session = requests.Session()
        r = session.get(URL_API, headers=HEADERS, timeout=15)
        dados = r.json()
        
        # Lê a lista de registros
        records = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if records:
            # 1. LISTA VERTICAL (Sem bolinhas, como você quer)
            with area_lista.container():
                for p in records[:12]:
                    nome = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-cor c-{p["color"]}">{nome} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 2. SINAL DIRETO (Sem firulas de 10 pretos)
            ultima = records[0]
            cor_alvo = "VERMELHO 🔴" if ultima['color'] == 2 else "PRETO ⚫"
            if ultima['color'] == 0: cor_alvo = "AGUARDAR..."

            with area_sinal.container():
                st.markdown(f"""
                    <div class="painel-sinal">
                        <h2 style="color: #00ff00;">SINAL CONFIRMADO</h2>
                        <div style="font-size: 50px; font-weight: bold; margin: 20px 0;">{cor_alvo}</div>
                        <p style="background:white; color:black; padding:10px; border-radius:5px; font-weight:bold; display:inline-block;">COBRIR BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS (Usa o created_at que você mandou)
            with area_terminais.container():
                brancos = [d for d in records if d['color'] == 0]
                for b in brancos[:8]:
                    horario = b['created_at'][11:16]
                    st.markdown(f"""
                        <div class="card-terminal">
                            <small style="color:#666;">BRANCO ÀS:</small><br>
                            <b style="font-size:26px;">{horario}</b>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            area_sinal.warning("Aguardando novos dados da plataforma...")

    except Exception as e:
        area_sinal.error("Reconectando ao servidor...")
    
    time.sleep(5)
