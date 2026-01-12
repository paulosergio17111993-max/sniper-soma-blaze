import streamlit as st

# Configuração da página para ficar estilo Aplicativo de Celular
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="centered")

# --- ESTILO GAMER NEON (CSS CUSTOMIZADO) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00ffc8;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff0055, #7000ff);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 10px;
        font-weight: bold;
        text-transform: uppercase;
        box-shadow: 0 0 15px #7000ff;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 30px #ff0055;
        transform: scale(1.02);
    }
    input {
        background-color: #1a1c23 !important;
        color: #00ffc8 !important;
        border: 1px solid #7000ff !important;
    }
    h1 {
        text-align: center;
        text-shadow: 2px 2px #ff0055;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SENHA ---
SENHA_CORRETA = "VIP777" # <--- Escolha sua senha aqui

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO")
    st.write("---")
    senha = st.text_input("DIGITE A CHAVE DE ATIVAÇÃO:", type="password")
    if st.button("DESBLOQUEAR ALGORITMO"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ CHAVE INVÁLIDA!")
    st.stop()

# --- PAINEL DO ROBÔ (VISUAL GAMER) ---
st.markdown("<h1>🎯 SNIPER: SOMA PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Análise de Peso de Pedra v2.0</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

with col1:
    pedra = st.number_input("Nº DA PEDRA:", min_value=0, max_value=14, step=1)

with col2:
    minuto = st.number_input("MINUTO ATUAL:", min_value=0, max_value=59, step=1)

st.write("")
if st.button("🔥 CALCULAR ENTRADA AGORA"):
    resultado = pedra + minuto
    if resultado >= 60:
        resultado -= 60
    
    st.markdown(f"""
        <div style="background: rgba(112, 0, 255, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #00ffc8; text-align: center;">
            <h2 style="color: white; margin: 0;">🎯 ALVO CONFIRMADO</h2>
            <h1 style="color: #00ffc8; font-size: 50px; margin: 10px 0;">MINUTO {resultado:02d}</h1>
            <p style="color: #ff0055; font-weight: bold;">⚠️ ENTRAR 1 MINUTO ANTES E DEPOIS</p>
        </div>
    """, unsafe_allow_html=True)

st.write("---")
st.caption("© 2026 Algoritmo Soma Pro - Todos os direitos reservados.")
