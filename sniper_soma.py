import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO VISUAL RAIZ ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical (Coluna 1) */
    .caixa-cor {
        padding: 10px; border-radius: 5px; margin-bottom: 5px;
        font-weight: bold; text-align: center; font-size: 15px;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 8px #fff; }
    .c-1 { background-color: #f12c4c; color: #fff; }
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Painel de Sinal (Coluna 2) */
    .painel-entrada {
        background: #000; border: 3px solid #00ff00;
        border-radius: 20px; padding: 45px; text-align: center;
        box-shadow: 0 0 20px rgba(0,255,0,0.2);
    }
    
    /* Terminais de Branco (Coluna 3) */
    .card-terminal {
        background: #111; border-left: 4px solid #ffffff;
        padding: 12px; margin-bottom: 8px; border-radius: 0 8px 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

# Layout de 3 Colunas como o antigo
col1, col2, col3 = st.columns([1, 1.8, 1])

with col1:
    st.markdown("### 🕒 CORES")
    area_cores = st.empty()

with col2:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()

with col3:
    st.markdown("### ⚪ TERMINAIS")
    area_terminais = st.empty()

URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        r = requests.get(URL_API, timeout=10)
        # O robô agora lê a lista que você enviou
        dados = r.json() 
        if not isinstance(dados, list):
            dados = dados.get('records', [])
        
        if dados:
            # 1. LISTA VERTICAL DE CORES (Esquerda)
            with area_cores.container():
                for p in dados[:15]:
                    nome = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-cor c-{p["color"]}">{nome} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 2. SINAL CENTRAL (Análise de Tendência)
            ultima = dados[0]
            # Sugere a cor oposta à última que saiu (Estratégia Sniper)
            sugerida = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="painel-entrada">
                        <h2 style="color: #00ff00; margin:0;">SINAL CONFIRMADO</h2>
                        <div style="font-size: 45px; font-weight: bold; margin: 20px 0;">{sugerida}</div>
                        <p style="background: white; color: black; padding: 8px; display: inline-block; border-radius: 5px; font-weight: bold;">
                            PROTEGER NO BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS VICIADOS (Direita) - Extrai o horário do seu JSON
            with area_terminais.container():
                brancos = [d for d in dados if d['color'] == 0]
                if brancos:
                    for b in brancos[:10]:
                        # Extrai HH:MM do campo created_at
                        horario = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <small style="color: #888;">BRANCO IDENTIFICADO</small><br>
                                <b style="font-size: 22px;">{horario}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Monitorando brancos...")

    except:
        pass
    
    time.sleep(5)
