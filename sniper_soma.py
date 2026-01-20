import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical */
    .caixa-cor {
        padding: 12px; border-radius: 6px; margin-bottom: 6px;
        font-weight: bold; text-align: center; font-size: 16px;
        text-transform: uppercase;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; } /* Branco */
    .c-1 { background-color: #f12c4c; color: #fff; } /* Vermelho */
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; } /* Preto */

    /* Terminais de Branco (Horários) */
    .card-terminal {
        background: #111; border-left: 5px solid #ffffff;
        padding: 15px; margin-bottom: 10px; border-radius: 0 10px 10px 0;
    }
    
    /* Painel de Sinal Central */
    .alerta-entrada {
        background: #000; border: 3px solid #00ff00;
        border-radius: 20px; padding: 50px; text-align: center;
        box-shadow: 0 0 25px rgba(0,255,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 SNIPER MS PRO")

# Layout de 3 Colunas (Lista | Sinal | Terminais)
col1, col2, col3 = st.columns([1, 1.8, 1])

with col1:
    st.markdown("### 🕒 HISTÓRICO")
    area_historico = st.empty()

with col2:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()

with col3:
    st.markdown("### ⚪ TERMINAIS")
    area_terminais = st.empty()

URL_API = "https://api.smashup.com/api/v1/games/double/history"

while True:
    try:
        # Puxando os dados da API que você mandou
        r = requests.get(URL_API, timeout=10)
        dados = r.json()
        
        # Garantindo que estamos lendo a lista de registros
        records = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if records:
            # 1. LISTA DE CORES VERTICAL (Baseado no seu JSON)
            with area_historico.container():
                for p in records[:15]:
                    nome = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-cor c-{p["color"]}">{nome} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 2. SINAL CENTRAL (Lógica de Cor)
            ultima = records[0]
            # Estratégia: Se veio Preto, entra Vermelho (e vice-versa)
            cor_sinal = "VERMELHO 🔴" if ultima['color'] == 2 else "PRETO ⚫"
            if ultima['color'] == 0: cor_sinal = "AGUARDAR GIRO..."

            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-entrada">
                        <h1 style="color: #00ff00; margin:0;">SINAL CONFIRMADO</h1>
                        <div style="font-size: 50px; font-weight: bold; margin: 25px 0;">{cor_sinal}</div>
                        <p style="background: white; color: black; padding: 10px; border-radius: 5px; font-weight: bold; display: inline-block;">
                            COBRIR O BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS VICIADOS (Extraindo os horários dos Brancos do seu JSON)
            with area_terminais.container():
                brancos = [d for d in records if d['color'] == 0]
                if brancos:
                    for b in brancos[:8]:
                        # Pega o campo 'created_at' e isola a hora (HH:MM)
                        horario = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <span style="color: #666; font-size: 12px;">BRANCO ÀS:</span><br>
                                <b style="font-size: 24px;">{horario}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Monitorando Brancos...")

    except Exception as e:
        st.error("Erro ao conectar na API...")
    
    time.sleep(5)
