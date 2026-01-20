import streamlit as st
import requests
import time

# --- NOVO VISUAL SNIPER (SÓ BRANCOS E SINAL) ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

# Forçando o fundo a ser bem preto para destacar
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #ffffff; }
    
    .alerta-central {
        background: #000; border: 5px solid #00ff00;
        border-radius: 30px; padding: 60px; text-align: center;
        box-shadow: 0 0 40px rgba(0,255,0,0.3);
    }
    
    .card-branco {
        background: #111; border: 1px solid #ffffff;
        padding: 15px; border-radius: 12px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
    
    .bola-0 {
        width: 35px; height: 35px; background: #fff; color: #000;
        border-radius: 5px; display: flex; align-items: center; 
        justify-content: center; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Link da sua API
URL_API = "https://api.smashup.com/api/v1/games/double/history"

st.title("🏹 SNIPER MS PRO - VERSÃO 2.0")

col1, col2 = st.columns([2, 1])

with col1:
    area_sinal = st.empty()

with col2:
    st.subheader("⚪ HISTÓRICO DE BRANCOS")
    area_brancos = st.empty()

while True:
    try:
        # Busca os dados reais
        r = requests.get(URL_API, timeout=5)
        # Entra na lista 'records' do JSON
        dados = r.json().get('records', [])
        
        if dados:
            # 1. PEGA A COR DA ÚLTIMA RODADA
            ultima = dados[0]
            cor_atual = "PRETO ⚫" if ultima['color'] == 2 else "VERMELHO 🔴"
            if ultima['color'] == 0: cor_atual = "BRANCO ⚪"

            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-central">
                        <h2 style="color: #00ff00; letter-spacing: 3px;">🎯 ENTRADA IDENTIFICADA</h2>
                        <div style="font-size: 60px; font-weight: bold; margin: 20px 0;">{cor_atual}</div>
                        <div style="background: #ffffff; color: #000; padding: 10px; border-radius: 10px; font-weight: bold; display: inline-block;">
                            COBRIR O BRANCO ⚪
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # 2. LISTA SÓ OS BRANCOS (ROLL 0)
            with area_brancos.container():
                brancos = [d for d in dados if d['roll'] == 0]
                if brancos:
                    for b in brancos[:12]: # Mostra os últimos 12 brancos
                        # Pega só a hora e minuto
                        hora_formatada = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-branco">
                                <div class="bola-0">0</div>
                                <div style="font-weight: bold;">BRANCO SAIU</div>
                                <div style="color: #00ff00;">{hora_formatada}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Aguardando sair branco no site...")

    except Exception as e:
        st.error("Conectando ao servidor da plataforma...")

    time.sleep(3)
