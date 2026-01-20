import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE INTERFACE LIMPA ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores Vertical (Padrão Antigo) */
    .caixa-cor {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .c-1 { background-color: #f12c4c; color: #fff; }
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Estilo dos Terminais Viciados */
    .card-terminal {
        background: #111; border-left: 6px solid #00ff00;
        padding: 20px; margin-bottom: 12px; border-radius: 0 5px 5px 0;
    }
    
    /* Painel de Sinal Central */
    .painel-sinal {
        background: #000; border: 3px solid #00ff00;
        border-radius: 15px; padding: 60px; text-align: center;
        box-shadow: 0 0 20px rgba(0,255,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Título Original
st.title("🏹 SNIPER MS PRO - OPERACIONAL")

# Layout de 3 Colunas: Cores | Sinal | Terminais
col1, col2, col3 = st.columns([1, 1.8, 1])

with col1:
    st.markdown("### 🕒 LISTA DE CORES")
    area_lista = st.empty()

with col2:
    st.markdown("### 🎯 PRÓXIMA ENTRADA")
    area_sinal = st.empty()

with col3:
    st.markdown("### ⚪ TERMINAIS (BRANCO)")
    area_brancos = st.empty()

# Configuração de Conexão Estável
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}

while True:
    try:
        # Busca dados da API que você enviou
        r = requests.get(URL_API, headers=HEADERS, timeout=15)
        r.raise_for_status()
        dados = r.json()
        records = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if records:
            # 1. LISTA DE CORES VERTICAL (Sem bolinhas)
            with area_lista.container():
                for p in records[:12]:
                    nome = "BRANCO" if p['color'] == 0 else ("VERMELHO" if p['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-cor c-{p["color"]}">{nome} ({p["roll"]})</div>', unsafe_allow_html=True)

            # 2. SINAL CENTRAL (Sem contagens de pedras)
            ultima = records[0]
            sinal = "VERMELHO 🔴" if ultima['color'] == 2 else "PRETO ⚫"
            if ultima['color'] == 0: sinal = "AGUARDAR..."

            with area_sinal.container():
                st.markdown(f"""
                    <div class="painel-sinal">
                        <h1 style="color: #00ff00; margin:0;">ENTRADA CONFIRMADA</h1>
                        <div style="font-size: 55px; font-weight: bold; margin: 30px 0;">{sinal}</div>
                        <p style="background: white; color: black; padding: 10px; font-weight: bold; display: inline-block; border-radius: 5px;">
                            COBRIR O BRANCO ⚪
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. TERMINAIS VICIADOS (Horários Reais)
            with area_brancos.container():
                brancos = [d for d in records if d['color'] == 0]
                if brancos:
                    for b in brancos[:8]:
                        # Extrai HH:MM do campo created_at do seu JSON
                        horario = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <small style="color: #666;">HORÁRIO VICIADO</small><br>
                                <b style="font-size: 28px;">{horario}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Buscando padrões...")

    except Exception:
        # Se a conexão falhar, mostra o aviso que você viu
        area_sinal.warning("Falha na conexão. A plataforma pode estar instável. Tentando reconectar...")
    
    time.sleep(5)
