import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE CORES E ESTILO ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Histórico de Bolinhas (O que você não quer perder) */
    .historico-container {
        display: flex; flex-wrap: nowrap; overflow-x: auto;
        padding: 15px; background: #111; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 20px;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 5px; color: white;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } /* Branco */
    .cor-1 { background-color: #f12c4c; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; border: 1px solid #444; } /* Preto */

    /* Alerta de Sinal */
    .alerta-sniper {
        background: #000; border: 3px solid #00ff00;
        border-radius: 20px; padding: 40px; text-align: center;
        box-shadow: 0 0 20px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

URL_API = "https://api.smashup.com/api/v1/games/double/history"

st.title("🏹 SNIPER MS PRO")

# Áreas de atualização
area_hist = st.empty()
col1, col2 = st.columns([2, 1])
with col1: area_sinal = st.empty()
with col2: area_brancos = st.empty()

while True:
    try:
        r = requests.get(URL_API, timeout=5)
        dados = r.json().get('records', [])
        
        if dados:
            # 1. MOSTRA O HISTÓRICO DE CORES (LISTA ORIGINAL)
            with area_hist.container():
                st.write("🕒 ÚLTIMOS RESULTADOS:")
                html_hist = '<div class="historico-container">'
                for p in dados[:20]: # Mostra as últimas 20 pedras
                    html_hist += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html_hist += '</div>'
                st.markdown(html_hist, unsafe_allow_html=True)

            # 2. SINAL CENTRAL
            ultima = dados[0]
            cor_txt = "PRETO ⚫" if ultima['color'] == 2 else "VERMELHO 🔴"
            if ultima['color'] == 0: cor_txt = "BRANCO ⚪"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-sniper">
                        <h2 style="color: #00ff00;">🎯 ENTRADA CONFIRMADA</h2>
                        <div style="font-size: 50px; font-weight: bold;">{cor_txt}</div>
                        <p>PROTEGER NO BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. LISTA DE BRANCOS
            with area_brancos.container():
                st.write("⚪ ÚLTIMOS BRANCOS:")
                brancos = [d for d in dados if d['roll'] == 0]
                for b in brancos[:5]:
                    st.success(f"BRANCO: {b['created_at'][11:16]}")

    except:
        pass
    
    time.sleep(3)
