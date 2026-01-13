import streamlit as st
import datetime

# Configuração da página
st.set_page_config(page_title="ALGORITMO SOMA PRO", layout="centered")

# --- ESTILO GAMER NEON ---
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
        border-left: 5px solid #00ffc8; margin-bottom: 10px;
    }
    h1 { text-align: center; text-shadow: 2px 2px #7000ff; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE SENHA ---
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
st.write("---")

col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", min_value=0, max_value=14, step=1)
with col2:
    minuto = st.number_input("MINUTO ATUAL:", min_value=0, max_value=59, step=1)

if st.button("🔥 GERAR SINAL SNIPER"):
    # Efeito de Carregamento
    with st.spinner('Analisando peso das pedras...'):
        import time
        time.sleep(1) # Simula o algoritmo pensando
        
        resultado = (pedra + minuto) % 60
        agora = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Adiciona ao histórico (no topo da lista)
        novo_sinal = f"ALVO: Minuto {resultado:02d} (Gerado às {agora})"
        st.session_state.historico.insert(0, novo_sinal)
        
    st.markdown(f"""
        <div style="background: rgba(112, 0, 255, 0.3); padding: 20px; border-radius: 15px; border: 2px solid #00ffc8; text-align: center;">
            <h2 style="color: white; margin: 0;">🎯 ALVO CONFIRMADO</h2>
            <h1 style="color: #00ffc8; font-size: 50px; margin: 10px 0;">MINUTO {resultado:02d}</h1>
        </div>
    """, unsafe_allow_html=True)

# --- SEÇÃO DE HISTÓRICO ---
st.write("")
st.subheader("📋 Últimos Sinais Gerados")

if st.session_state.historico:
    for sinal in st.session_state.historico[:5]: # Mostra os últimos 5
        st.markdown(f'<div class="historico-card">{sinal}</div>', unsafe_allow_html=True)
    
    if st.button("Limpar Histórico"):
        st.session_state.historico = []
        st.rerun()
else:
    st.write("Nenhum sinal gerado nesta sessão.")

st.write("---")
st.caption("Focado na Estratégia de Soma de Pesos.")
