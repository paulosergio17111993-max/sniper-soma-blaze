import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA CHEIA (Estilo Algoritmo-Soma-Pro) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #080808; color: white; }
    
    /* Coluna de Cores Vertical */
    .linha-cor {
        padding: 10px; margin-bottom: 5px; border-radius: 4px;
        text-align: center; font-weight: bold; font-size: 14px;
    }
    .cor-0 { background: #ffffff; color: #000; border: 1px solid #ccc; }
    .cor-1 { background: #f12c4c; color: #fff; }
    .cor-2 { background: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Cartão de Horário (Terminais) */
    .card-terminal {
        background: #151515; border-left: 5px solid #00ff00;
        padding: 15px; margin-bottom: 8px; border-radius: 4px;
    }
    
    /* Painel de Sinal Central */
    .box-sinal {
        background: #000; border: 2px solid #00ff00;
        padding: 40px; text-align: center; border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

# Criando as 3 colunas laterais
col_historico, col_principal, col_terminais = st.columns([1, 1.8, 1])

with col_historico:
    st.subheader("🕒 LISTA CORES")
    area_lista = st.empty()

with col_principal:
    st.subheader("🎯 MONITORAMENTO")
    area_entrada = st.empty()

with col_terminais:
    st.subheader("⚪ HORÁRIOS BRANCO")
    area_brancos = st.empty()

URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        r = requests.get(URL_API, timeout=10)
        dados = r.json()
        
        # Lendo a lista de rodadas
        registros = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if registros:
            # 1. LISTA VERTICAL DE CORES (Esquerda)
            with area_lista.container():
                for r in registros[:15]:
                    cor_id = r['color']
                    num = r['roll']
                    label = "BRANCO" if cor_id == 0 else ("VERMELHO" if cor_id == 1 else "PRETO")
                    st.markdown(f'<div class="linha-cor cor-{cor_id}">{label} ({num})</div>', unsafe_allow_html=True)

            # 2. SINAL DE ENTRADA (Centro)
            ultima = registros[0]
            entrada = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with area_entrada.container():
                st.markdown(f"""
                    <div class="box-sinal">
                        <h2 style="color: #00ff00;">SINAL IDENTIFICADO</h2>
                        <div style="font-size: 45px; font-weight: bold; margin: 15px 0;">{entrada}</div>
                        <p style="background: white; color: black; padding: 5px; font-weight: bold; display: inline-block; border-radius: 4px;">
                            PROTEGER NO BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS VICIADOS (Direita) - Extrai o HH:MM do created_at
            with area_brancos.container():
                lista_brancos = [i for i in registros if i['color'] == 0]
                if lista_brancos:
                    for b in lista_brancos[:8]:
                        # Pega o horário 01:03 do JSON que você mandou
                        hora_minuto = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <small style="color: #888;">TERMINAL CONFIRMADO</small><br>
                                <b style="font-size: 24px;">{hora_minuto}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Monitorando horários...")

    except:
        st.warning("Reconectando ao servidor...")

    time.sleep(5)
