import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="SISTEMA SOMA PRO", layout="centered")

# --- ESTILO VISUAL (IGUAL ÀS FOTOS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card-geral {
        background-color: white; border-radius: 8px; padding: 12px; margin-bottom: 8px;
        display: flex; justify-content: space-between; align-items: center;
        border-left: 10px solid #7000ff; color: black; font-weight: bold;
    }
    .alerta-soma {
        background: white; color: black; padding: 20px; border-radius: 15px;
        text-align: center; font-weight: bold; border: 5px solid #7000ff; margin-bottom: 20px;
    }
    .estrelas { color: #f1c40f; }
    h1, h3 { color: #00ffc8; text-align: center; margin-top: 20px; }
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

# --- MEMÓRIA DO PAINEL ---
if 'exibir_soma' not in st.session_state: st.session_state.exibir_soma = False
if 'exibir_cores' not in st.session_state: st.session_state.exibir_cores = False
if 'exibir_branco' not in st.session_state: st.session_state.exibir_branco = False

# --- ENTRADA DE DADOS ---
st.markdown("<h1>🎯 SISTEMA SOMA PRO</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", 0, 14, step=1)
with col2:
    min_atual = st.number_input("MINUTO ATUAL:", 0, 59, step=1)

# Lógica de Horário
fuso = pytz.timezone('America/Sao_Paulo')
agora = datetime.datetime.now(fuso)
intervalos = [4, 8, 12, 16, 20]

# --- BOTÕES DE COMANDO ---
st.write("---")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔥 SOMA DA PEDRA"): st.session_state.exibir_soma = True
with c2:
    if st.button("📋 LISTA CORES"): st.session_state.exibir_cores = True
with c3:
    if st.button("⚪ LISTA BRANCO"): st.session_state.exibir_branco = True

if st.button("🗑️ LIMPAR TELA"):
    st.session_state.exibir_soma = st.session_state.exibir_cores = st.session_state.exibir_branco = False
    st.rerun()

# --- ÁREA DE EXIBIÇÃO (SÓ APARECE SE CLICAR) ---

# 1. QUADRO DA SOMA (COR DA PEDRA)
if st.session_state.exibir_soma:
    min_soma = (pedra + min_atual) % 60
    if 1 <= pedra <= 7:
        c_nome, c_hex = "VERMELHO 🔴", "red"
    elif pedra >= 8:
        c_nome, c_hex = "PRETO ⚫", "black"
    else:
        c_nome, c_hex = "BRANCO ⚪", "gray"
        
    st.markdown(f"""
        <div class="alerta-soma">
            <p style="margin:0;">🎯 ALVO DE COR IDENTIFICADO</p>
            <h1 style="margin:5px 0; font-size:45px; color: {c_hex};">{c_nome}</h1>
            <h2 style="color: black; margin:0;">MINUTO: {min_soma:02d}</h2>
            <p style="margin-top:10px; font-size:12px; color: #7000ff;">ESTRATEGIA SOMA PRO</p>
        </div>
    """, unsafe_allow_html=True)

# 2. LISTA DE BRANCO (ESTILO FOTO)
if st.session_state.exibir_branco:
    st.markdown("<h3>📋 LISTA ASSERTIVA - BRANCO ⚪</h3>", unsafe_allow_html=True)
    for t in intervalos:
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span>BRANCO ⚪</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)

# 3. LISTA DE CORES (ALTERNADA)
if st.session_state.exibir_cores:
    st.markdown("<h3>📋 PRÓXIMAS CORES ASSERTIVAS 🔴⚫</h3>", unsafe_allow_html=True)
    for i, t in enumerate(intervalos):
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        c_txt, c_hex = ("VERMELHO 🔴", "red") if i % 2 == 0 else ("PRETO ⚫", "black")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span style="color:{c_hex}">{c_txt}</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)

st.write("---")
st.markdown("<p style='text-align:center; color:white; font-size:12px;'>⚠️ Use sempre a proteção no branco!</p>", unsafe_allow_html=True)
