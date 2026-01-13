import streamlit as st
import datetime
import pytz

# Configuração da página
st.set_page_config(page_title="SISTEMA SOMA PRO", layout="centered")

# --- ESTILO VISUAL (CSS) ---
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

# --- MEMÓRIA DOS BOTÕES ---
if 'show_soma' not in st.session_state: st.session_state.show_soma = False
if 'show_cores' not in st.session_state: st.session_state.show_cores = False
if 'show_branco' not in st.session_state: st.session_state.show_branco = False

# --- ENTRADA ---
st.markdown("<h1>🎯 SISTEMA SOMA PRO</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    pedra = st.number_input("Nº DA PEDRA:", 0, 14, step=1)
with col2:
    min_atual = st.number_input("MINUTO ATUAL:", 0, 59, step=1)

# Lógica de Cor da Pedra
if 1 <= pedra <= 7:
    cor_alvo, emoji_alvo, css_cor = "VERMELHO", "🔴", "red"
elif pedra >= 8:
    cor_alvo, emoji_alvo, css_cor = "PRETO", "⚫", "black"
else:
    cor_alvo, emoji_alvo, css_cor = "BRANCO", "⚪", "gray"

# --- BOTÕES ---
st.write("---")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔥 SOMA DA PEDRA"): st.session_state.show_soma = True
with c2:
    if st.button("📋 LISTA CORES"): st.session_state.show_cores = True
with c3:
    if st.button("⚪ LISTA BRANCO"): st.session_state.show_branco = True

if st.button("🗑️ LIMPAR"):
    st.session_state.show_soma = st.session_state.show_cores = st.session_state.show_branco = False
    st.rerun()

# --- EXIBIÇÃO ---

# 1. RESULTADO DA SOMA (APENAS CORES)
if st.session_state.show_soma:
    min_soma = (pedra + min_atual) % 60
    st.markdown(f"""
        <div class="alerta-soma">
            <p style="margin:0; font-size: 18px;">🎯 SINAL DE COR IDENTIFICADO</p>
            <h1 style="margin:5px 0; font-size:45px; color: {css_cor};">{cor_alvo} {emoji_alvo}</h1>
            <h2 style="color: black; margin:0;">MINUTO: {min_soma:02d}</h2>
            <p style="margin-top:10px; font-size:12px; color: #7000ff;">PROTEGER NO BRANCO ⚪</p>
        </div>
    """, unsafe_allow_html=True)

# 2. LISTA DE CORES (ALTERNADA)
if st.session_state.show_cores:
    st.markdown("<h3>📋 LISTA DE CORES (ALTERNADA)</h3>", unsafe_allow_html=True)
    agora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    for i, t in enumerate([4, 8, 12, 16, 20]):
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        c_txt, c_hex = ("VERMELHO 🔴", "red") if i % 2 == 0 else ("PRETO ⚫", "black")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span style="color:{c_hex}">{c_txt}</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)

# 3. LISTA DE BRANCO
if st.session_state.show_branco:
    st.markdown("<h3>⚪ LISTA EXCLUSIVA BRANCO</h3>", unsafe_allow_html=True)
    agora = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    for t in [4, 8, 12, 16, 20]:
        h = (agora + datetime.timedelta(minutes=t)).strftime("%H:%M")
        st.markdown(f'<div class="card-geral"><span>⏰ {h}</span><span style="color:gray">BRANCO ⚪</span><span class="estrelas">⭐⭐⭐⭐⭐</span></div>', unsafe_allow_html=True)
