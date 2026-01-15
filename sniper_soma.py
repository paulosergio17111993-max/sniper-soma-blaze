import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - OPERAÇÃO COMPLETA", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-alerta { 
        background: #161b22; border: 2px solid #00ff88; padding: 20px; 
        border-radius: 10px; text-align: center; margin-bottom: 20px;
    }
    .radar-box { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 15px; margin-bottom: 8px; border-left: 5px solid #00ff88; font-size: 20px;
        font-weight: bold;
    }
    .branco-box {
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 15px; margin-bottom: 8px; border-left: 5px solid #ffffff; font-size: 20px;
        font-weight: bold; color: #aaa;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'l_sinais' not in st.session_state: st.session_state.l_sinais = []

# --- MOTOR DE CÁLCULO ---
def calcular_primeira_cor(pedra):
    # REGRA PAULO: 1 a 7 = Vermelho | 8 a 14 = Preto
    if 1 <= pedra <= 7:
        return "VERMELHO 🔴"
    elif 8 <= pedra <= 14:
        return "PRETO ⚫"
    return "BRANCO ⚪"

def gerar_ciclo_completo(min_inicio, cor_inicial):
    agora = datetime.now(fuso_ms)
    referencia = agora.replace(minute=min_inicio, second=0, microsecond=0)
    
    if referencia < agora:
        referencia += timedelta(hours=1)
        
    lista = []
    cor_atual = cor_inicial
    
    for i in range(4):
        lista.append({
            "h": referencia.strftime("%H:%M"), 
            "cor": cor_atual,
            "branco": "BRANCO ⚪"
        })
        # Alternância de Cor
        cor_atual = "PRETO ⚫" if cor_atual == "VERMELHO 🔴" else "VERMELHO 🔴"
        referencia += timedelta(minutes=4)
    return lista

# --- INTERFACE ---
st.title("🎯 SNIPER MS - MODO OPERAÇÃO COMPLETA")

col_cores, col_brancos, col_ctrl = st.columns([1, 1, 1])

with col_ctrl:
    st.subheader("⌨️ DADOS DA MESA")
    p_atual = st.number_input("PEDRA QUE SAIU:", 0, 14, 7)
    m_atual = st.number_input("MINUTO DO RELÓGIO:", 0, 59, 17)
    
    min_calc = (m_atual + p_atual) % 60
    cor_ini = calcular_primeira_cor(p_atual)
    
    st.markdown(f"""
        <div class="box-alerta">
            <small>INÍCIO DA SEQUÊNCIA:</small><br>
            <h2 style="color:#00ff88; margin:0;">{cor_ini}</h2>
            <h3 style="margin:0;">Horário: :{min_calc:02d}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ GERAR LISTA COMPLETA", use_container_width=True):
        st.session_state.l_sinais = gerar_ciclo_completo(min_calc, cor_ini)

    if st.button("🗑️ LIMPAR", use_container_width=True):
        st.session_state.l_sinais = []
        st.rerun()

with col_cores:
    if st.session_state.l_sinais:
        st.subheader("🔥 CORES (ALTERNADAS)")
        for s in st.session_state.l_sinais:
            cor_borda = "#ff4b4b" if "🔴" in s['cor'] else "#ffffff" if "⚪" in s['cor'] else "#444"
            st.markdown(f'<div class="radar-box" style="border-left-color:{cor_borda};">⏰ {s["h"]} | {s["cor"]}</div>', unsafe_allow_html=True)

with col_brancos:
    if st.session_state.l_sinais:
        st.subheader("⚪ PROTEÇÃO BRANCO")
        for s in st.session_state.l_sinais:
            st.markdown(f'<div class="branco-box">⏰ {s["h"]} | {s["branco"]}</div>', unsafe_allow_html=True)
