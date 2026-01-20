import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-container {
        display: flex; justify-content: center; padding: 15px;
        background: #111; border-radius: 10px; margin-bottom: 25px;
    }
    .bola {
        width: 38px; height: 38px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 6px;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .cor-1 { background-color: #f12c4c; color: white; }
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; }
    .alerta-sniper {
        background: #000; border: 4px solid #00ff00;
        border-radius: 20px; padding: 50px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

area_topo = st.empty()
area_meio = st.empty()

# URL DA API E HEADERS PARA EVITAR BLOQUEIO
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

while True:
    try:
        # Tenta buscar com headers de um navegador real
        r = requests.get(URL_API, headers=HEADERS, timeout=10)
        dados = r.json().get('records', [])
        
        if dados:
            # 1. MOSTRA AS BOLINHAS (HISTÓRICO)
            with area_topo.container():
                st.write("🕒 ÚLTIMOS RESULTADOS:")
                html_bolas = '<div class="historico-container">'
                for p in dados[:14]:
                    html_bolas += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html_bolas += '</div>'
                st.markdown(html_bolas, unsafe_allow_html=True)

            # 2. MOSTRA O SINAL
            ultima = dados[0]
            sugestao = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_meio.container():
                st.markdown(f"""
                    <div class="alerta-sniper">
                        <h2 style="color: #00ff00; margin: 0;">SINAL CONFIRMADO</h2>
                        <div style="font-size: 55px; font-weight: bold; margin: 15px 0;">{sugestao}</div>
                        <p style="background: #fff; color: #000; padding: 10px; border-radius: 8px; font-weight: bold; display: inline-block;">
                            COBRIR O BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            area_meio.warning("Conectado, aguardando dados...")

    except Exception as e:
        area_meio.error("⚠️ Falha na conexão com a plataforma. Tentando burlar o bloqueio...")

    time.sleep(5)
