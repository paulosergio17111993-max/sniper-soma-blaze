import streamlit as st
import requests
import time

# --- CONFIGURAÇÃO DE INTERFACE LIMPA (SOMA PRO) ---
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    
    /* Lista de Cores em Formato de Tabela Vertical (Sem bolinhas) */
    .caixa-lista {
        padding: 15px; border-radius: 4px; margin-bottom: 8px;
        text-align: center; font-weight: bold; font-size: 18px;
        text-transform: uppercase;
    }
    .c-0 { background-color: #ffffff; color: #000; box-shadow: 0 0 10px #fff; }
    .c-1 { background-color: #f12c4c; color: #fff; }
    .c-2 { background-color: #2b2b2b; color: #fff; border: 1px solid #444; }

    /* Horários dos Terminais (Branco) */
    .card-terminal {
        background: #111; border-left: 6px solid #00ff00;
        padding: 20px; margin-bottom: 12px; border-radius: 4px;
    }
    
    /* Painel Central de Sinal */
    .quadro-sinal {
        background: #000; border: 3px solid #00ff00;
        border-radius: 15px; padding: 60px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 ALGORITMO SOMA PRO")

# Layout de 3 Colunas Originais
col_cores, col_entrada, col_terminais = st.columns([1, 1.8, 1])

with col_cores:
    st.markdown("### 🕒 LISTA CORES")
    area_lista = st.empty()

with col_entrada:
    st.markdown("### 🎯 ENTRADA")
    area_sinal = st.empty()

with col_terminais:
    st.markdown("### ⚪ TERMINAIS")
    area_brancos = st.empty()

# --- CONEXÃO COM DISFARCE DE NAVEGADOR ---
URL_API = "https://api.smashup.com/api/v1/games/double/history"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Accept": "application/json"
}

while True:
    try:
        # Tenta buscar os dados com cabeçalhos reais para evitar bloqueio
        response = requests.get(URL_API, headers=HEADERS, timeout=15)
        dados = response.json()
        
        # Garante que está lendo a lista de registros enviada
        registros = dados.get('records', []) if isinstance(dados, dict) else dados
        
        if registros:
            # 1. PREENCHE A LISTA VERTICAL (Lado Esquerdo)
            with area_lista.container():
                for item in registros[:12]:
                    txt = "BRANCO" if item['color'] == 0 else ("VERMELHO" if item['color'] == 1 else "PRETO")
                    st.markdown(f'<div class="caixa-lista c-{item["color"]}">{txt} ({item["roll"]})</div>', unsafe_allow_html=True)

            # 2. GERA O SINAL (Centro)
            ultima_cor = registros[0]['color']
            sugestao = "VERMELHO 🔴" if ultima_cor == 2 else "PRETO ⚫"
            
            with area_sinal.container():
                st.markdown(f"""
                    <div class="quadro-sinal">
                        <h1 style="color: #00ff00; margin:0;">ENTRADA CONFIRMADA</h1>
                        <div style="font-size: 55px; font-weight: bold; margin: 30px 0;">{sugestao}</div>
                        <p style="background: white; color: black; padding: 8px; border-radius: 4px; font-weight: bold; display: inline-block;">PROTEGER NO BRANCO ⚪</p>
                    </div>
                """, unsafe_allow_html=True)

            # 3. MOSTRA OS TERMINAIS (Lado Direito)
            with area_brancos.container():
                lista_brancos = [d for d in registros if d['color'] == 0]
                if lista_brancos:
                    for b in lista_brancos[:8]:
                        # Extrai HH:MM do campo created_at
                        horario = b['created_at'][11:16]
                        st.markdown(f"""
                            <div class="card-terminal">
                                <small style="color: #666;">BRANCO IDENTIFICADO</small><br>
                                <b style="font-size: 28px;">{horario}</b>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("Aguardando padrão...")
        else:
            area_sinal.warning("Aguardando novos dados...")

    except Exception:
        # Se falhar, mantém a mensagem de reconexão que você viu
        area_sinal.warning("Reconectando ao servidor... Verifique sua conexão.")
    
    time.sleep(5)
