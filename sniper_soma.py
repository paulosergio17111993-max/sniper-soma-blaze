import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER 4 SINAIS", layout="wide")

# --- MEMÓRIA ---
if 'cor_entrada' not in st.session_state: st.session_state.cor_entrada = "Aguardando Soma..."
if 'l_cores' not in st.session_state: st.session_state.l_cores = []
if 'l_brancos' not in st.session_state: st.session_state.l_brancos = []

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-entrada { background: #161b22; border: 2px solid #00ff88; padding: 15px; border-radius: 10px; text-align: center; }
    .radar-box { background-color: #10141d; border: 1px solid #1d2633; border-radius: 8px; padding: 12px; margin-bottom: 5px; border-left: 5px solid #00ff88; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE GERAÇÃO (4 SINAIS - PULO DE 4 MIN) ---
def gerar_proximos_sinais(tipo, min_base, cor_base, lista_atual):
    agora = datetime.now(fuso_ms)
    
    # Se já existir uma lista, o novo sinal começa 4 min após o último da lista
    if lista_atual:
        ultimo_horario = datetime.strptime(lista_atual[-1]['h'], "%H:%M")
        referencia = agora.replace(hour=ultimo_horario.hour, minute=ultimo_horario.minute, second=0) + timedelta(minutes=4)
    else:
        # Se for a primeira vez, começa no minuto da soma
        referencia = agora.replace(minute=min_base, second=0, microsecond=0)
        if referencia < agora:
            referencia += timedelta(hours=1)
    
    nova_remessa = []
    for i in range(4): # APENAS 4 SINAIS
        msg = f"ENTRADA: {cor_base}" if tipo == "COR" else "ENTRADA: BRANCO ⚪"
        nova_remessa.append({"h": referencia.strftime("%H:%M"), "msg": msg})
        referencia = referencia + timedelta(minutes=4)
        
    return nova_remessa

# --- INTERFACE ---
st.title("🎯 SNIPER MS - CICLO DE 4 SINAIS")

col_lista, col_ctrl = st.columns([2, 1])

with col_ctrl:
    st.subheader("🧮 SOMA MESTRA")
    p_pedra = st.number_input("PEDRA:", 0, 14, 5)
    p_minuto = st.number_input("MINUTO:", 0, 59, 10)
    
    if st.button("🔥 SOMAR PEDRA + MINUTO", use_container_width=True):
        total = p_pedra + p_minuto
        st.session_state.cor_entrada = "VERMELHO 🔴" if total % 2 == 0 else "PRETO ⚫"
    
    st.markdown(f"""
        <div class="box-entrada">
            <small>COR GERADA:</small><br>
            <h2 style="color:#00ff88;">{st.session_state.cor_entrada}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # BOTÕES DE GERAÇÃO
    if st.button("➕ GERAR MAIS CORES (4 SINAIS)", use_container_width=True):
        if "🔴" in st.session_state.cor_entrada or "⚫" in st.session_state.cor_entrada:
            st.session_state.l_cores = gerar_proximos_sinais("COR", p_minuto, st.session_state.cor_entrada, st.session_state.l_cores)
            
    if st.button("➕ GERAR MAIS BRANCOS (4 SINAIS)", use_container_width=True):
        st.session_state.l_brancos = gerar_proximos_sinais("BRANCO", p_minuto, "", st.session_state.l_brancos)

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_cores = []; st.session_state.l_brancos = []
        st.session_state.cor_entrada = "Aguardando Soma..."
        st.rerun()

with col_lista:
    if st.session_state.l_cores:
        st.subheader("🔥 SEQUÊNCIA DE CORES (PULO 4M)")
        for s in st.session_state.l_cores:
            st.markdown(f'<div class="radar-box">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)

    if st.session_state.l_brancos:
        st.subheader("⚪ SEQUÊNCIA DE BRANCOS (PULO 4M)")
        for s in st.session_state.l_brancos:
            st.markdown(f'<div class="radar-box" style="border-left-color:white;">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)
