import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: white; }
    .painel-aviso {
        border: 2px solid #333; padding: 20px; text-align: center; border-radius: 10px;
    }
    .bola {
        width: 40px; height: 40px; border-radius: 5px;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: bold; margin: 5px;
    }
    .cor-0 { background-color: #ffffff; color: #000; }
    .cor-1 { background-color: #f12c4c; color: white; }
    .cor-2 { background-color: #2b2b2b; color: white; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO - STATUS: ATIVO")

# Criando espaços vazios para preencher depois
espaco_historico = st.empty()
espaco_sinal = st.empty()

# URL DA API
URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # 1. Tenta buscar os dados
        r = requests.get(URL_API, timeout=10)
        dados = r.json().get('records', [])
        
        if dados:
            # 2. MOSTRA O HISTÓRICO (Bolinhas)
            with espaco_historico.container():
                st.write("### 🕒 ÚLTIMOS RESULTADOS")
                conteudo_html = '<div style="background: #111; padding: 15px; border-radius: 10px; margin-bottom: 20px;">'
                for p in dados[:14]:
                    conteudo_html += f'<div class="bola cor-{p["color"]}">{p["roll"]}</div>'
                conteudo_html += '</div>'
                st.markdown(conteudo_html, unsafe_allow_html=True)

            # 3. MOSTRA O SINAL
            ultima = dados[0]
            cor_alvo = "PRETO ⚫" if ultima['color'] == 1 else "VERMELHO 🔴"
            
            with espaco_sinal.container():
                st.markdown(f"""
                    <div style="background: #000; border: 4px solid #00ff00; padding: 40px; text-align: center; border-radius: 20px;">
                        <h2 style="color: #00ff00;">🎯 ENTRADA CONFIRMADA</h2>
                        <div style="font-size: 50px; font-weight: bold; margin: 20px 0;">{cor_alvo}</div>
                        <div style="background: #fff; color: #000; padding: 10px; border-radius: 5px; font-weight: bold; display: inline-block;">
                            PROTEGER NO BRANCO ⚪
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            espaco_sinal.warning("Conectado, mas aguardando dados da Smash...")

    except Exception as e:
        espaco_sinal.error(f"Erro de Conexão: O site da plataforma pode estar fora do ar.")

    time.sleep(5)
