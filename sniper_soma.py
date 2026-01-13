import streamlit as st
import datetime
import pytz # Biblioteca para o horário de Brasília

# Configuração da página
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="centered")

# --- ESTILO GAMER COM CORES DE ALVO ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ffc8; }
    .stButton>button {
        width: 100%; background: linear-gradient(45deg, #00ffc8, #7000ff);
        color: white; border: none; padding: 12px; border-radius: 10px;
        font-weight: bold; box-shadow: 0 0 15px #7000ff;
    }
    .historico-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px; border-radius: 8px;
        margin-bottom: 10px; font-family: monospace;
    }
    h1 { text-align: center; text-shadow: 2px 2px #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SENHA E MEMÓRIA ---
SENHA_CORRETA = "VIP777"
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "historico" not in st.session_state:
    st.session_state.historico = []

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO")
    senha = st.text_input("CHAVE DE ATIVAÇÃO:", type="password")
    if st.button("DESBLOQUEAR"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- PAINEL PRINCIPAL ---
st.markdown("<h1>🎯 SNIPER: SOMA PRO</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", min_value=0, max_value=14, step=1)
with col2:
    minuto = st.number_input("MINUTO ATUAL:", min_value=0, max_value=59, step=1)

if st.button("🔥 GERAR SINAL SNIPER"):
    # 1. PEGAR HORA DE BRASÍLIA
    fuso_br = pytz.timezone('America/Sao_Paulo')
    agora_br = datetime.datetime.now(fuso_br).strftime("%H:%M:%S")
    
    # 2. CÁLCULO DO ALVO
    resultado = (pedra + minuto) % 60
    
    # 3. LÓGICA DA COR (Personalize se quiser)
    if pedra == 0:
        cor_nome = "BRANCO ⚪"
        cor_hex = "#ffffff"
    elif pedra % 2 == 0:
        cor_nome = "VERMELHO 🔴"
        cor_hex = "#ff0055"
    else:
        cor_nome = "PRETO ⚫"
        cor_hex = "#000000"
    
    # 4. SALVAR NO HISTÓRICO
    sinal_texto = f"⏰ {agora_br} | 🎯 Min {resultado:02d} | {cor_nome}"
    st.session_state.historico.insert(0, sinal_texto)
    
    # 5. MOSTRAR ALVO GRANDE NA TELA
    st.markdown(f"""
        <div style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px; border: 3px solid {cor_hex}; text-align: center;">
            <h2 style="color: white; margin: 0;">ALVO: MINUTO {resultado:02d}</h2>
            <h1 style="color: {cor_hex}; font-size: 40px; margin: 10px 0;">{cor_nome}</h1>
            <p style="color: #00ffc8;">Gerado às: {agora_br}</p>
        </div>
    """, unsafe_allow_html=True)

# --- SEÇÃO DE HISTÓRICO ---
st.write("---")
st.subheader("📋 Últimos Sinais Gerados")

for s in st.session_state.historico[:5]:
    st.markdown(f'<div class="historico-card">{s}</div>', unsafe_allow_html=True)

if st.button("Limpar Histórico"):
    st.session_state.historico = []
    st.rerun()
