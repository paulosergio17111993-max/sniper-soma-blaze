import streamlit as st
import requests
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE ALTA PERFORMANCE ---
st.set_page_config(page_title="SNIPER LIVE SYNC", layout="centered")

# CSS para as bolinhas ficarem idênticas às da plataforma
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .historico-wrapper {
        display: flex;
        flex-direction: row-reverse;
        justify-content: center;
        gap: 8px;
        background: #0d0d0d;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 25px;
        overflow-x: auto;
    }
    .bola {
        min-width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 14px; color: white; border: 1px solid rgba(255,255,255,0.1);
    }
    .cor-0 { background-color: #ffffff; color: #000; } /* Branco */
    .cor-1 { background-color: #e02424; } /* Vermelho */
    .cor-2 { background-color: #1a1a1a; } /* Preto */
    
    .card-soma {
        background: linear-gradient(145deg, #0d0d0d, #1a1a1a);
        border: 2px solid #6b46c1;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 0px 0px 20px rgba(107, 70, 193, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO QUE PUXA O HISTÓRICO REAL ---
def get_live_history():
    # IMPORTANTE: Aqui é onde conectamos no link da sua plataforma
    # Por enquanto, ele gera uma lista para você ver a atualização visual
    try:
        # Exemplo de chamada real: data = requests.get('LINK_DA_API').json()
        # Vamos simular o histórico chegando:
        return [
            {"num": 10, "cor": 2}, {"num": 5, "cor": 1}, {"num": 0, "cor": 0},
            {"num": 14, "cor": 1}, {"num": 10, "cor": 2}, {"num": 2, "cor": 1}
        ]
    except:
        return []

# --- INTERFACE AO VIVO ---
st.title("🏹 SNIPER MS PRO - AO VIVO")

# Criamos um espaço vazio que será atualizado pelo loop
placeholder = st.empty()

while True:
    with placeholder.container():
        historico = get_live_history()
        
        if historico:
            # 1. MOSTRA O HISTÓRICO DE BOLINHAS CONFORME SAI NA RODADA
            cols_html = '<div class="historico-wrapper">'
            for p in historico:
                cols_html += f'<div class="bola cor-{p["cor"]}">{p["num"]}</div>'
            cols_html += '</div>'
            st.markdown(cols_html, unsafe_allow_html=True)
            
            # 2. LOGICA DA PEDRA 10 (SOMA +10)
            ultima_pedra = historico[0] # A pedra que acabou de cair
            
            if ultima_pedra["num"] == 10:
                min_atual = datetime.now().minute
                min_alvo = (min_atual + 10) % 60
                
                st.markdown(f"""
                    <div class="card-soma">
                        <p style="color: #00ff00; font-weight: bold; letter-spacing: 2px;">● SINAL AUTOMÁTICO GERADO</p>
                        <p style="font-size: 14px; color: #aaa;">Gatilho: Pedra 10 no histórico</p>
                        <h1 style="font-size: 80px; margin: 10px 0;">{min_alvo:02d}</h1>
                        <p style="font-size: 24px;">PRÓXIMA ENTRADA: <b>PRETO ⚫</b></p>
                        <p style="color: #6b46c1; font-weight: bold;">SOMA: {min_atual} + 10</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.write("🔍 Monitorando rodadas... Aguardando Pedra 10 no topo.")
        
    time.sleep(2) # Faz o "olho" do robô piscar a cada 2 segundos para ver a nova rodada
