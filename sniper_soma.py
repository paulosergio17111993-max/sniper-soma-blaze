import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO RAIZ (O começo de tudo) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical (Sem Bolinhas) */
    .caixa-item {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
        text-transform: uppercase;
    }
    .cor-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .cor-1 { background-color: #f12c4c; color: #fff; }
    .cor-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Estilo dos Terminais (Coluna Direita) */
    .terminal-raiz {
        background: #111; border-left: 6px solid #00ff00;
        padding: 20px; margin-bottom: 12px; border-radius: 0 5px 5px 0;
    }
    
    /* Painel Central */
    .alerta-soma {
        background: #000; border: 3px solid #00ff00;
        border-radius: 15px; padding: 60px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# Título conforme sua imagem
st.title("🏹 SNIPER MS PRO - OPERACIONAL")

# O layout de 3 colunas que você conhece
col_cores, col_sinal, col_terminais = st.columns([1, 1.8, 1])

with col_cores:
    st.markdown("### 🕒 LISTA DE CORES")
    area_lista = st.empty()

with col_sinal:
    st.markdown("### 🎯 PRÓXIMA ENTRADA")
    area_sinal = st.empty()

with col_terminais:
    st.markdown("### ⚪ TERMINAIS (BRANCO)")
    area_brancos = st.empty()

# URL que puxa os dados do JSON que você me mandou
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {"User-Agent": "Mozilla/5.0"}

while True:
    try:
        r = requests.get(URL_API, headers=HEADERS, timeout=10)
        dados = r.json()
        
        # Lendo a lista de rodadas exatamente como você mandou
        records = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if records:
            # 1. PREENCHE A LISTA VERTICAL (Sem bolinhas, só a caixa colorida)
            with area_lista.container():
                for p in records[:12]:
                    txt = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-item cor-{p["color"]}">{txt} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 2. GERA O SINAL CENTRAL (Sem contagens de "10 pretos", só o sinal)
            ultima = records[0]
            sinal_cor = "VERMELHO 🔴" if ultima['color'] == 2 else "PRETO ⚫"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="alerta-soma">
                        <h1 style="color: #00ff00; margin:0;">ENTRADA CONFIRMADA</h1>
                        <div style="font-size: 55px; font-weight: bold; margin: 30px 0;">{sinal_cor}</div>
                        <p style="background: white; color: black; padding: 10px; font-weight: bold; display: inline-block;">PROTEGER NO BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. FILTRA OS TERMINAIS DE BRANCO (Pelo horário que você mandou)
            with area_terminais.container():
                brancos = [d for d in records if d['color'] == 0]
                if brancos:
                    for b in brancos[:8]:
                        # Pega o horário HH:MM (ex: 01:03)
                        horario = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="terminal-raiz">
                                <small style="color: #555;">HORÁRIO VICIADO</small><br>
                                <b style="font-size: 28px;">{horario}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Buscando padrões...")

    except:
        # Mostra a mensagem de reconexão se a API cair
        area_sinal.warning("Reconectando ao servidor...")
    
    time.sleep(5)
