import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE CORES E ESTILO (O que estava no seu GitHub) ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Histórico de Bolinhas Original */
    .historico-container {
        display: flex; flex-direction: row; justify-content: center;
        padding: 20px; background: #111; border-radius: 10px;
        border: 1px solid #333; margin: 20px 0;
    }
    .bola {
        width: 40px; height: 40px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 8px; font-size: 18px;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } 
    .cor-1 { background-color: #f12c4c; color: white; } 
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; }

    /* Alerta Sniper Central */
    .alerta-sniper {
        background: #000; border: 4px solid #00ff00;
        border-radius: 25px; padding: 50px; text-align: center;
        box-shadow: 0 0 30px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# URL DA API REAL
URL_API = "https://api.smashup.com/api/v1/games/double/history"

st.title("🏹 SNIPER MS PRO")

# Áreas fixas para evitar que a tela fique vazia
area_hist = st.empty()
area_sinal = st.empty()

while True:
    try:
        r = requests.get(URL_API, timeout=5)
        dados = r.json().get('records', [])
        
        if dados:
            # 1. DESENHA O HISTÓRICO DE BOLINHAS NO TOPO
            with area_hist.container():
                html_hist = '<div class="historico-container">'
                for p in dados[:15]: # Últimas 15 pedras
                    html_hist += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html_hist += '</div>'
                st.markdown(html_hist, unsafe_allow_html=True)

            # 2. DESENHA O SINAL DE ENTRADA CENTRAL
            ultima = dados[0]
            # Lógica simples: Se a última foi Preta, entra Vermelha (ou vice-versa)
            sugerida = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-sniper">
                        <h1 style="color: #00ff00; margin: 0;">SINAL CONFIRMADO</h1>
                        <p style="color: #888; font-size: 20px;">ENTRADA AGORA EM:</p>
                        <div style="font-size: 60px; font-weight: bold; margin: 15px 0;">{sugerida}</div>
                        <div style="background: #fff; color: #000; padding: 10px; border-radius: 8px; display: inline-block; font-weight: bold;">
                            PROTEGER NO BRANCO ⚪
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Aguardando dados da plataforma...")

    except Exception as e:
        st.error("Erro de conexão. Tentando reconectar...")
    
    time.sleep(3)
