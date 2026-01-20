import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Layout das Bolinhas (O que você pediu para manter) */
    .historico-container {
        display: flex; justify-content: center; padding: 15px;
        background: #111; border-radius: 10px; margin-bottom: 25px;
    }
    .bola {
        width: 38px; height: 38px; border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 6px; font-size: 16px;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } /* Branco */
    .cor-1 { background-color: #f12c4c; color: white; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; } /* Preto */

    /* Alerta Central Gigante */
    .alerta-sniper {
        background: #000; border: 4px solid #00ff00;
        border-radius: 20px; padding: 50px; text-align: center;
        box-shadow: 0 0 30px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

# Áreas reservadas para os dados aparecerem
area_topo = st.empty()
area_meio = st.empty()

URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # Busca os dados reais da plataforma
        r = requests.get(URL_API, timeout=8)
        dados = r.json().get('records', [])
        
        if dados:
            # 1. MOSTRA AS BOLINHAS (HISTÓRICO)
            with area_topo.container():
                st.write("🕒 ÚLTIMOS RESULTADOS:")
                html_bolas = '<div class="historico-container">'
                for p in dados[:14]: # Mostra as últimas 14
                    html_bolas += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html_bolas += '</div>'
                st.markdown(html_bolas, unsafe_allow_html=True)

            # 2. MOSTRA O SINAL DE ENTRADA (LÓGICA LIMPA)
            ultima = dados[0]
            # Se a última foi preto (2), sugere vermelho (1). Se foi vermelho, sugere preto.
            sugestao = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_meio.container():
                st.markdown(f"""
                    <div class="alerta-sniper">
                        <h2 style="color: #00ff00; margin: 0;">SINAL CONFIRMADO</h2>
                        <div style="font-size: 55px; font-weight: bold; margin: 15px 0;">{sugestao}</div>
                        <div style="background: #fff; color: #000; padding: 12px; border-radius: 8px; font-weight: bold; display: inline-block;">
                            COBRIR O BRANCO ⚪
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            area_meio.info("Conectado. Aguardando a próxima rodada...")

    except:
        area_meio.error("⚠️ Erro de conexão com a SmashUp. Tentando reconectar...")

    time.sleep(4)
