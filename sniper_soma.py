import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE TELA E ESTILO ANTIGO ---
st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores (Vertical) */
    .item-historico {
        padding: 10px; border-radius: 5px; margin-bottom: 5px;
        font-weight: bold; text-align: center; text-transform: uppercase;
    }
    .bg-0 { background-color: #ffffff; color: #000; } /* Branco */
    .bg-1 { background-color: #f12c4c; color: #fff; } /* Vermelho */
    .bg-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; } /* Preto */

    /* Terminais de Branco (Lista Lateral) */
    .card-branco {
        background: #111; border-left: 4px solid #fff;
        padding: 10px; margin-bottom: 8px; border-radius: 0 5px 5px 0;
    }
    
    /* Alerta de Entrada */
    .alerta-entrada {
        background: #000; border: 3px solid #00ff00;
        border-radius: 15px; padding: 30px; text-align: center;
        box-shadow: 0 0 15px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# URL DA API
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {"User-Agent": "Mozilla/5.0"}

st.title("🏹 SNIPER MS PRO - OPERACIONAL")

# LAYOUT EM COLUNAS (Como era antes)
col1, col2, col3 = st.columns([1.5, 1, 1])

with col1:
    st.subheader("🎯 PRÓXIMA ENTRADA")
    area_sinal = st.empty()

with col2:
    st.subheader("🕒 LISTA DE CORES")
    area_cores = st.empty()

with col3:
    st.subheader("⚪ TERMINAIS (BRANCO)")
    area_brancos = st.empty()

while True:
    try:
        r = requests.get(URL_API, headers=HEADERS, timeout=10)
        dados = r.json().get('records', [])
        
        if dados:
            # 1. SINAL DE ENTRADA
            ultima = dados[0]
            cor_nome = "PRETO ⚫" if ultima['color'] == 2 else "VERMELHO 🔴"
            if ultima['color'] == 0: cor_nome = "BRANCO ⚪"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-entrada">
                        <div style="color: #00ff00; font-weight: bold;">SINAL ANALISADO</div>
                        <div style="font-size: 35px; margin: 15px 0;">{cor_nome}</div>
                        <div style="font-size: 14px; color: #888;">PROTEGER NO BRANCO (0)</div>
                    </div>
                """, unsafe_allow_html=True)

            # 2. LISTA DE CORES (VERTICAL)
            with area_cores.container():
                for p in dados[:12]:
                    txt = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="item-historico bg-{p["color"]}">{txt} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 3. LISTA DE BRANCOS (TERMINAIS VICIADOS)
            with area_brancos.container():
                brancos = [d for d in dados if d['color'] == 0]
                if brancos:
                    for b in brancos[:10]:
                        hora = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-branco">
                                <div style="font-size: 12px; color: #aaa;">BRANCO CONFIRMADO</div>
                                <div style="font-weight: bold; font-size: 18px;">{hora}</div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Monitorando terminais...")

    except:
        pass

    time.sleep(5)
