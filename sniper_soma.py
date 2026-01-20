import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE ESTILO ---
st.set_page_config(page_title="SNIPER LIVE", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .historico-wrapper {
        display: flex; flex-direction: row; background: #111;
        padding: 10px; border-radius: 8px; border: 1px solid #333;
        margin-bottom: 20px; overflow-x: auto;
    }
    .bola {
        min-width: 35px; height: 35px; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 0 4px;
    }
    .cor-1 { background-color: #f12c4c; } /* Vermelho */
    .cor-2 { background-color: #2b2b2b; border: 1px solid #444; } /* Preto */
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    .card-sinal {
        background: #000; border: 2px solid #00ff00;
        border-radius: 15px; padding: 25px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

# Áreas que vão mudar na tela
espaco_hist = st.empty()
espaco_sinal = st.empty()

# O LINK DA SUA API (SMASH)
URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # 1. PEGA OS DADOS
        response = requests.get(URL_API, timeout=5)
        json_completo = response.json()
        
        # 2. ENTRA NA "CAIXA" RECORDS (Onde os dados que você mandou ficam)
        lista_pedras = json_completo.get('records', [])

        if lista_pedras:
            # MOSTRA AS BOLINHAS
            with espaco_hist.container():
                st.write("🕒 ÚLTIMAS RODADAS:")
                html = '<div class="historico-wrapper">'
                for p in lista_pedras[:15]:
                    html += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

            # 3. PROCURA A PEDRA 10 E FAZ A CONTA
            achou_10 = False
            for item in lista_pedras:
                if item['roll'] == 10:
                    # Pega o minuto do 'created_at' (Ex: 23:28:58 -> pega o 28)
                    tempo_raw = item['created_at'].split('T')[1]
                    minuto_pedra = int(tempo_raw.split(':')[1])
                    
                    minuto_alvo = (minuto_pedra + 10) % 60
                    
                    with espaco_sinal.container():
                        st.markdown(f"""
                            <div class="card-sinal">
                                <h3 style="color: #00ff00;">🎯 SINAL CONFIRMADO</h3>
                                <p>Pedra 10 identificada no minuto {minuto_pedra:02d}</p>
                                <h1 style="font-size: 80px; margin: 10px 0;">{minuto_alvo:02d}</h1>
                                <p style="font-size: 20px;">ENTRADA: <b>PRETO ⚫</b></p>
                                <p style="color: #6b46c1;">Lógica: {minuto_pedra} + 10</p>
                            </div>
                        """, unsafe_allow_html=True)
                    achou_10 = True
                    break
            
            if not achou_10:
                espaco_sinal.info("🔎 Analisando histórico... Aguardando Pedra 10.")

    except Exception as e:
        st.error(f"Aguardando conexão com a plataforma...")

    time.sleep(3) # Atualiza a cada 3 segundos
