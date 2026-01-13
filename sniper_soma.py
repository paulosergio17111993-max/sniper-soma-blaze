import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="SISTEMA SOMA PRO", layout="centered")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card-branco {
        background-color: white; border-radius: 8px; padding: 12px; margin-bottom: 8px;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 10px solid #7000ff; color: black; font-weight: bold;
    }
    .alerta-soma {
        background: white; color: black; padding: 20px; border-radius: 15px;
        text-align: center; font-weight: bold; border: 5px solid #7000ff; margin-bottom: 25px;
    }
    .estrelas { color: #f1c40f; }
    h1, h3 { color: #00ffc8; text-align: center; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 ACESSO RESTRITO")
    senha = st.text_input("CHAVE VIP:", type="password")
    if st.button("ENTRAR"):
        if senha == "VIP777":
            st.session_state.autenticado = True
            st.rerun()
    st.stop()

# --- INTERFACE DE ENTRADA ---
st.markdown("<h1>🎯 SISTEMA SOMA PRO</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", 0, 14, step=1)
with col2:
    min_atual = st.number_input("MINUTO ATUAL:", 0, 59, step=1)

# Configuração de Horário
fuso = pytz.timezone('America/Sao_Paulo')
agora = datetime.datetime.now(fuso)
intervalos = [4, 8, 12, 16, 20]

st.write("---")

# --- BOTÕES LADO A LADO ---
c1, c2, c3 = st.columns(3)

# Inicializa estados para os botões não sumirem
if 'ver_soma' not in st.session_state: st.session_state.ver_soma = False
if 'ver_cores' not in st.session_state: st.session_state.ver_cores = False
if 'ver_branco' not in st.session_state: st.session_state.ver_branco = False

with c1:
    if st.button("🔥 SINAL ÚNICO"):
        st.session_state.ver_soma = True
        st.session_state.ver_cores = False
        st.session_state.ver_branco = False
with c2:
    if st.button("📋 LISTA CORES"):
        st.session_state.ver_cores = True
        st.session_state.ver_soma = False
        st.session_state.ver_branco = False
with c3:
    if st.button("⚪ LISTA BRANCO"):
        st.session_state.ver_branco = True
        st.session_state.ver_soma = False
        st.session_state.ver_cores = False

# --- ÁREA DE RESULTADO (CADA UM NO SEU CANTO) ---

if st.session_state.ver_soma:
    alvo = (pedra + min_atual) % 60
    st.markdown(f"""
        <div class="alerta-soma">
            <p style="margin:0; font-size: 18px;">⚪ ALVO NO BRANCO IDENTIFICADO ⚪</p>
            <h1 style="margin:5px 0; font-size:50px; color: black;">MINUTO: {alvo:02d}</h1>
            <p style="margin:0; color: #7000ff;">ESTRATEGIA SOMA PRO</p>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.ver_cores:
    st.markdown("<h3>📋 PRÓXIMAS CORES ASSERTIVAS</h3>", unsafe_allow_html=True)
    for i, tempo in enumerate(intervalos):
        prox = agora + datetime.timedelta(minutes=tempo)
        h_fmt = prox.strftime("%H:%M")
        # Alternância do seu arquivo original
        cor_txt, cor_css = ("VERMELHO 🔴", "red") if i % 2 == 0 else ("PRETO ⚫", "black")
        estrelas = "⭐⭐⭐⭐⭐" if i < 2 else "⭐⭐⭐⭐"
        st.markdown(f"""
            <div class="card-branco">
                <span>⏰ {h_fmt}</span>
                <span style="color:{cor_css}">{cor_txt}</span>
                <span class="estrelas">{estrelas}</span>
            </div>
        """, unsafe_allow_html=True)

if st.session_state.ver_branco:
    st.markdown("<h3>📝 LISTA ASSERTIVA - BRANCO ⚪</h3>", unsafe_allow_html=True)
    for i, tempo in enumerate(intervalos):
        prox = agora + datetime.timedelta(minutes=tempo)
        h_fmt = prox.strftime("%H:%M")
        estrelas = "⭐⭐⭐⭐⭐" if i < 2 else "⭐⭐⭐⭐"
        st.markdown(f"""
            <div class="card-branco">
                <span>⏰ {h_fmt}</span>
                <span style="color:gray">BRANCO ⚪</span>
                <span class="estrelas">{estrelas}</span>
            </div>
        """, unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align:center; color:white; font-size:12px;'>⚠️ Use sempre a proteção no branco!</p>", unsafe_allow_html=True)
