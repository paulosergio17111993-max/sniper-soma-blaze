
    import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="centered")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    /* Estilo do Alerta de Branco */
    .alerta-branco {
        background: white;
        color: black;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        border-left: 15px solid #7000ff;
        border-right: 15px solid #7000ff;
        margin-bottom: 25px;
    }
    /* Estilo dos Cards da Lista de Cores */
    .card-cor {
        background-color: white;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 8px solid #7000ff;
        color: black;
        font-weight: bold;
    }
    .estrelas { color: #f1c40f; }
    h1, h3 { color: #00ffc8; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if not st.session_state.autenticado:
    senha = st.text_input("CHAVE VIP:", type="password")
    if st.button("ENTRAR"):
        if senha == "VIP777":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- ENTRADA ---
st.markdown("<h1>🎯 ANALISADOR SOMA PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", 0, 14, step=1)
with col2:
    min_atual = st.number_input("MINUTO ATUAL:", 0, 59, step=1)

if st.button("🔥 GERAR SINAIS"):
    # --- 1. CÁLCULO DO BRANCO (FOCO PRINCIPAL) ---
    alvo_branco = (pedra + min_atual) % 60
    
    st.markdown(f"""
        <div class="alerta-branco">
            <p style="margin:0; font-size: 18px;">⚪ ALVO NO BRANCO IDENTIFICADO ⚪</p>
            <h1 style="margin:5px 0; font-size:45px; color: black;">MINUTO: {alvo_branco:02d}</h1>
            <p style="margin:0; color: #7000ff;">ESTRATEGIA SOMA PRO</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. LISTA DE CORES (CONFORME O SEU ARQUIVO) ---
    st.markdown("<h3>📋 PRÓXIMAS CORES ASSERTIVAS</h3>", unsafe_allow_html=True)
    
    fuso = pytz.timezone('America/Sao_Paulo')
    agora = datetime.datetime.now(fuso)
    intervalos = [4, 8, 12, 16, 20] # Seus intervalos originais
    
    for i, tempo in enumerate(intervalos):
        prox = agora + datetime.timedelta(minutes=tempo)
        h_fmt = prox.strftime("%H:%M")
        
        # Alternando cores: Vermelho, Preto, Vermelho...
        if i % 2 == 0:
            cor_nome, cor_css = "VERMELHO 🔴", "red"
        else:
            cor_nome, cor_css = "PRETO ⚫", "black"
            
        estrelas = "⭐⭐⭐⭐⭐" if i < 2 else "⭐⭐⭐⭐"
        
        st.markdown(f"""
            <div class="card-cor">
                <span>⏰ {h_fmt}</span>
                <span style="color: {cor_css};">{cor_nome}</span>
                <span class="estrelas">{estrelas}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<p style='text-align:center; color:white; font-size:12px;'>⚠️ Use sempre a proteção no branco em todas as entradas!</p>", unsafe_allow_html=True)
