import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000; color: white; }
    .coluna-cor {
        padding: 10px; border-radius: 5px; margin-bottom: 5px;
        text-align: center; font-weight: bold;
    }
    .c-0 { background: #fff; color: #000; }
    .c-1 { background: #f12c4c; color: #fff; }
    .c-2 { background: #333; color: #fff; border: 1px solid #555; }
    
    .card-branco {
        background: #111; border-left: 5px solid #fff;
        padding: 15px; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

# 1. Define onde as coisas vão aparecer
col_hist, col_sinal, col_brancos = st.columns([1, 1.5, 1])

with col_hist:
    st.subheader("🕒 CORES")
    area_lista = st.empty()

with col_sinal:
    st.subheader("🎯 SINAL")
    area_sinal = st.empty()

with col_brancos:
    st.subheader("⚪ BRANCOS")
    area_terminais = st.empty()

# URL DA API
URL = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # Puxa os dados
        r = requests.get(URL, timeout=10)
        dados = r.json()
        
        # Se os dados vierem como dicionário, pega a lista 'records'
        lista = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if lista:
            # --- PREENCHE A LISTA DE CORES ---
            with area_lista.container():
                for item in lista[:15]:
                    cor = item['color']
                    num = item['roll']
                    nome = "BRANCO" if cor == 0 else ("VERMELHO" if cor == 1 else "PRETO")
                    st.markdown(f'<div class="coluna-cor c-{cor}">{nome} ({num})</div>', unsafe_allow_html=True)

            # --- GERA O SINAL ---
            ultima = lista[0]
            sugestao = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div style="border: 3px solid #00ff00; padding: 40px; text-align: center; border-radius: 20px;">
                        <h1 style="color: #00ff00;">SINAL CONFIRMADO</h1>
                        <div style="font-size: 50px; font-weight: bold;">{sugestao}</div>
                        <p>COBRIR O BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # --- TERMINAIS DE BRANCO (Horários) ---
            with area_terminais.container():
                brancos = [i for i in lista if i['color'] == 0]
                for b in brancos[:8]:
                    hora = b['created_at'][11:16] # Pega HH:MM
                    st.markdown(f"""
                        <div class="card-branco">
                            <small style="color: #888;">HORÁRIO VICIADO</small><br>
                            <b style="font-size: 25px;">{hora}</b>
                        </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        # Se der erro, ele avisa na tela
        st.error(f"Aguardando conexão...")

    time.sleep(5)
