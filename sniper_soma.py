import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO VISUAL SNIPER ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Card do Sinal Principal */
    .card-sinal {
        background: #000;
        border: 3px solid #00ff00;
        border-radius: 20px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
    }
    
    .status-online {
        color: #00ff00;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 14px;
        letter-spacing: 2px;
    }

    .cor-entrada {
        font-size: 40px;
        font-weight: bold;
        margin: 20px 0;
    }

    /* Lista de Brancos */
    .item-branco {
        background: #111;
        border-left: 5px solid #fff;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .bola-branca {
        width: 35px; height: 35px; background: #fff;
        border-radius: 5px; color: #000;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE BUSCA NA API ---
URL_API = "https://api.smashup.com/api/v1/games/double/history"

def buscar_dados():
    try:
        r = requests.get(URL_API, timeout=5)
        return r.json().get('records', [])
    except:
        return []

# --- LAYOUT ---
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🏹 SNIPER MS PRO")
    area_sinal = st.empty()

with col2:
    st.markdown("### ⚪ HISTÓRICO DE BRANCOS")
    area_brancos = st.empty()

# --- LOOP AO VIVO ---
while True:
    dados = buscar_dados()
    
    if dados:
        # 1. ATUALIZA SINAL DE ENTRADA
        # (Aqui o sinal fica fixo ou baseado na última cor que saiu)
        ultima_cor = "PRETO ⚫" if dados[0]['color'] == 2 else "VERMELHO 🔴"
        
        with area_sinal.container():
            st.markdown(f"""
                <div class="card-sinal">
                    <div class="status-online">● Sniper Conectado</div>
                    <div style="font-size: 20px; margin-top: 10px;">PRÓXIMA ENTRADA:</div>
                    <div class="cor-entrada">{ultima_cor}</div>
                    <div style="background: #1a1a1a; padding: 10px; border-radius: 10px;">
                        <span style="color: #fff;">PROTEGER NO <b>BRANCO ⚪</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # 2. LISTA DE BRANCOS (Filtra apenas o roll 0)
        with area_brancos.container():
            brancos = [d for d in dados if d['roll'] == 0]
            if brancos:
                for b in brancos[:8]: # Mostra os últimos 8 brancos
                    hora = b['created_at'][11:16]
                    st.markdown(f"""
                        <div class="item-branco">
                            <div class="bola-branca">0</div>
                            <div style="font-weight: bold;">BRANCO CONFIRMADO</div>
                            <div style="color: #666;">{hora}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("Monitorando brancos...")

    time.sleep(3)
