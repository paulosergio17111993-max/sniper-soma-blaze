import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE DESIGN ---
st.set_page_config(page_title="SNIPER LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-wrapper {
        display: flex; flex-direction: row; background-color: #111;
        padding: 12px; border-radius: 8px; border: 1px solid #333;
        margin-bottom: 25px; overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 14px; color: white; margin-right: 8px;
    }
    .cor-1 { background-color: #f12c4c; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    
    .card-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 15px; padding: 30px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - LIVE")

# Áreas de atualização
placeholder_hist = st.empty()
placeholder_sinal = st.empty()

# URL da API (A que você me enviou os dados)
URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # Puxa os dados reais
        r = requests.get(URL_API, timeout=5)
        # ACESSA A CHAVE 'records' QUE VOCÊ ME MANDOU
        dados = r.json().get('records', [])
        
        if dados:
            # 1. ATUALIZA O HISTÓRICO VISUAL
            with placeholder_hist.container():
                st.write("🕒 HISTÓRICO AO VIVO:")
                html = '<div class="historico-wrapper">'
                for p in dados[:15]:
                    html += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

            # 2. LÓGICA DA SOMA 10
            # Vamos pegar a pedra 10 mais recente no histórico
            encontrou = False
            for item in dados:
                if item['roll'] == 10:
                    # Pega o minuto do campo 'created_at'
                    # Ex: 2026-01-19T23:28:58.381Z -> Pega o '28'
                    tempo_raw = item['created_at'].split('T')[1]
                    minuto_pedra = int(tempo_raw.split(':')[1])
                    
                    minuto_alvo = (minuto_pedra + 10) % 60
                    
                    with placeholder_sinal.container():
                        st.markdown(f"""
                            <div class="card-sinal">
                                <h3 style="color: #00ff00; margin:0;">🎯 SINAL IDENTIFICADO</h3>
                                <p style="color: #888;">Pedra 10 no minuto {minuto_pedra:02d}</p>
                                <h1 style="font-size: 85px; margin: 10px 0;">{minuto_alvo:02d}</h1>
                                <p style="font-size: 24px;">ENTRADA: <b>PRETO ⚫</b></p>
                                <p style="color: #6b46c1; font-weight: bold;">SOMA: {minuto_pedra} + 10</p>
                            </div>
                        """, unsafe_allow_html=True)
                    encontrou = True
                    break
            
            if not encontrou:
                placeholder_sinal.info("🔍 Monitorando... Aguardando Pedra 10.")
        else:
            st.error("API retornou vazia. Verifique o link.")

    except Exception as e:
        st.error(f"Erro de conexão: {e}")

    # Pausa de 3 segundos para não sobrecarregar
    time.sleep(3)
