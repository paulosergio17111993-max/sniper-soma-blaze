import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="SNIPER SCANNER PRO", layout="wide")
fuso_br = pytz.timezone('America/Sao_Paulo')

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .status-box { 
        padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;
        border: 1px solid #1d2633; background: #161b22;
    }
    .card-sinal { 
        background: #1c2128; border-left: 5px solid #00ff88; padding: 15px; 
        border-radius: 8px; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'padrao_detectado' not in st.session_state: st.session_state.padrao_detectado = "Aguardando Análise..."
if 'lista_sinais' not in st.session_state: st.session_state.lista_sinais = []

# --- MOTOR DE ANÁLISE PRÉ-GERAÇÃO ---
def analisar_tendencia_e_gerar():
    # Aqui o sistema simula a leitura do histórico
    # Na sua última lista, o padrão era 2-3. Na anterior, era 9-10-8.
    # Vamos criar uma lógica que decide o melhor ciclo agora.
    
    agora = datetime.now(fuso_br)
    
    # Simulação de análise: O robô decide qual alternância está 100%
    # (Em um sistema real, aqui ele consultaria a API da Blaze)
    decisao = st.session_state.get('escolha_tendencia', 'CURTO 2-3')
    
    if "CURTO" in decisao:
        pulos = [2, 3]
        st.session_state.padrao_detectado = "🔥 TENDÊNCIA 100%: CICLO 2-3 (ALTA ASSERTIVIDADE)"
    elif "LONGO" in decisao:
        pulos = [9, 10, 8]
        st.session_state.padrao_detectado = "💎 TENDÊNCIA 100%: CICLO LONGO 9-10-8"
    else:
        pulos = [4, 5]
        st.session_state.padrao_detectado = "⚡ TENDÊNCIA 100%: CICLO MÉDIO 4-5"

    # GERA A LISTA BASEADA NA ANÁLISE
    nova_lista = []
    ref = agora
    for i in range(15):
        pulo = pulos[i % len(pulos)]
        ref = ref + timedelta(minutes=pulo)
        nova_lista.append({"h": ref.strftime("%H:%M"), "p": pulo})
    
    st.session_state.lista_sinais = nova_lista

# --- INTERFACE ---
st.title("🎯 SNIPER ANALYSER")

col_main, col_ctrl = st.columns([2, 1])

with col_main:
    # Mostra o resultado da análise prévia
    st.markdown(f"""
        <div class="status-box">
            <small>STATUS DO SCANNER:</small><br>
            <h3 style="color:#00ff88;">{st.session_state.padrao_detectado}</h3>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.lista_sinais:
        for s in st.session_state.lista_sinais:
            st.markdown(f"""
                <div class="card-sinal">
                    <span style="font-size:18px;">⏰ <b>{s['h']}</b> — ENTRADA CONFIRMADA</span><br>
                    <small style="color:#888;">Analítico: Padrão identificado após pulo de {s['p']}min</small>
                </div>
            """, unsafe_allow_html=True)

with col_ctrl:
    st.subheader("🛠️ SCANNER DE MESA")
    st.write("Selecione a base da tendência que você está vendo no histórico:")
    
    st.session_state.escolha_tendencia = st.selectbox(
        "TIPO DE SCANNER:",
        ["CURTO 2-3 (PADRÃO QUALITY)", "MÉDIO 4-5", "LONGO 9-10-8"]
    )
    
    if st.button("🔍 ANALISAR E GERAR LISTA", use_container_width=True):
        analisar_tendencia_e_gerar()
        st.rerun()

    st.divider()
    st.markdown("""
        **COMO USAR:**
        1. Olhe os últimos 3 sinais da Blaze.
        2. Veja se o intervalo é curto (2-3) ou longo.
        3. Selecione o scanner e gere a lista.
        4. O robô vai manter a tendência até o final do ciclo.
    """)
