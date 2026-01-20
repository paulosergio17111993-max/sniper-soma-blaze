import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* PAINEL DE SINAL CENTRAL */
    .painel-central {
        background: #000; border: 3px solid #00ff00;
        border-radius: 20px; padding: 60px; text-align: center;
        box-shadow: 0 0 30px rgba(0, 255, 0, 0.2);
    }
    
    .status-badge { color: #00ff00; font-weight: bold; letter-spacing: 2px; }
    .texto-entrada { font-size: 50px; font-weight: bold; margin: 20px 0; color: #fff; }

    /* LISTA LATERAL DE BRANCOS */
    .card-branco {
        background: #111; border: 1px solid #fff;
        padding: 15px; border-radius: 10px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .bola-branca {
        width: 35px; height: 35px; background: #fff; color: #000;
        border-radius: 5px; display: flex; align-items: center; 
        justify-content: center; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Link da API que você mandou
URL_API = "https://api.smashup.com/api/v1/games/double/history"

col1, col2 = st.columns([2, 1])

with col1:
    st.title("🏹 SNIPER MS PRO")
    area_sinal = st.empty()

with col2:
    st.markdown("### ⚪ LISTA DE BRANCOS")
    area_brancos = st.empty()

while True:
    try:
        # Puxa os dados da API
        response = requests.get(URL_API, timeout=5)
        dados = response.json().get('records', [])
        
        if dados:
            # 1. MOSTRA O SINAL (Baseado na última pedra que saiu)
            ultima = dados[0]
            cor_nome = "PRETO ⚫" if ultima['color'] == 2 else "VERMELHO 🔴"
            if ultima['color'] == 0: cor_nome = "BRANCO ⚪"

            with area_sinal.container():
                st.markdown(f"""
                    <div class="painel-central">
                        <div class="status-badge">● CONECTADO AO VIVO</div>
                        <div style="font-size: 20px; color: #888; margin-top: 15px;">AGUARDANDO PRÓXIMA RODADA...</div>
                        <div class="texto-entrada">ENTRADA: {cor_nome}</div>
                        <div style="background: #1a1a1a; padding: 15px; border-radius: 10px; color: #fff;">
                            PROTEGER NO <b>BRANCO (0)</b>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            # 2. MOSTRA A LISTA DE BRANCOS (Filtra apenas quando roll é 0)
            with area_brancos.container():
                lista_brancos = [d for d in dados if d['roll'] == 0]
                if lista_brancos:
                    for b in lista_brancos[:10]: # Mostra os últimos 10
                        hora = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-branco">
                                <div class="bola-branca">0</div>
                                <div style="font-weight: bold;">BRANCO</div>
                                <div style="color: #666;">{hora}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Sem brancos recentes.")

    except Exception as e:
        st.error("Erro ao atualizar dados...")

    time.sleep(3) # Atualiza a cada 3 segundos
