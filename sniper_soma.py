import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="centered")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ffc8; }
    .stButton>button {
        width: 100%; background: linear-gradient(45deg, #00ffc8, #7000ff);
        color: white; border: none; padding: 12px; border-radius: 10px;
        font-weight: bold; box-shadow: 0 0 10px #7000ff;
    }
    .card-sinal {
        background: white; padding: 12px; border-radius: 8px; 
        color: #111; font-weight: bold; margin-bottom: 8px;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 8px solid #7000ff;
    }
    .resultado-unico {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px; border-radius: 15px; text-align: center;
        margin-top: 15px; border: 2px solid #00ffc8;
    }
    h1, h3 { text-align: center; color: #00ffc8; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
SENHA_CORRETA = "VIP777"
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO")
    senha = st.text_input("CHAVE DE ATIVAÇÃO:", type="password")
    if st.button("DESBLOQUEAR"):
        if senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- PAINEL PRINCIPAL ---
st.markdown("<h1>🎯 SNIPER & GERADOR VIP</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA ÚLTIMA PEDRA:", min_value=0, max_value=14, step=1)
with col2:
    minuto_input = st.number_input("MINUTO ATUAL:", min_value=0, max_value=59, step=1)

# Lógica de Cor (Pedra = Tendência)
if 1 <= pedra <= 7:
    cor_nome = "VERMELHO 🔴"
    cor_hex = "#ff4b4b"
    outra_cor = "PRETO ⚫"
elif pedra >= 8:
    cor_nome = "PRETO ⚫"
    cor_hex = "#1d1d1d"
    outra_cor = "VERMELHO 🔴"
else:
    cor_nome = "BRANCO ⚪"
    cor_hex = "#ffffff"
    outra_cor = "BRANCO ⚪"

# --- BOTÕES DE AÇÃO ---
tab1, tab2 = st.tabs(["🔥 SINAL ÚNICO", "📋 LISTA VIP"])

with tab1:
    if st.button("GERAR SINAL AGORA"):
        alvo = (pedra + minuto_input) % 60
        st.markdown(f"""
            <div class="resultado-unico">
                <p style="color: #ccc; margin: 0;">ENTRADA CONFIRMADA</p>
                <h1 style="color: {cor_hex}; font-size: 45px; margin: 5px 0;">{cor_nome}</h1>
                <h2 style="color: white; margin: 0;">MINUTO: {alvo:02d}</h2>
            </div>
        """, unsafe_allow_html=True)

with tab2:
    if st.button("GERAR LISTA COMPLETA"):
        st.markdown(f"### 📋 LISTA ASSERTIVA - {cor_nome}")
        fuso_br = pytz.timezone('America/Sao_Paulo')
        agora_br = datetime.datetime.now(fuso_br)
        
        intervalos = [4, 8, 12, 16, 20]
        
        for i, tempo in enumerate(intervalos):
            prox = agora_br + datetime.timedelta(minutes=tempo)
            h_format = prox.strftime("%H:%M")
            
            # Alterna a cor começando pela cor da pedra
            cor_atual = cor_nome if i % 2 == 0 else outra_cor
            estrelas = "⭐⭐⭐⭐⭐" if i < 2 else "⭐⭐⭐⭐"
            
            # Cor do texto no card
            cor_texto = "#ff4b4b" if "VERMELHO" in cor_atual else "#000"
            
            st.markdown(f"""
                <div class="card-sinal">
                    <span>⏰ {h_format}</span>
                    <span style="color: {cor_texto};">{cor_atual}</span>
                    <span style="color: #f1c40f;">{estrelas}</span>
                </div>
            """, unsafe_allow_html=True)
        st.caption("⚠️ Fazer proteção no Branco ⚪")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Sistema de Soma Pro v2.0</p>", unsafe_allow_html=True)
