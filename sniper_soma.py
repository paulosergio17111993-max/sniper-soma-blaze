import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - TESTE 100%", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-setup { 
        background: #161b22; border: 1px solid #30363d; padding: 20px; 
        border-radius: 10px; margin-bottom: 20px; border-top: 4px solid #00ff88;
    }
    .card-sinal { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; border-left: 8px solid #00ff88;
    }
    .cor-v { color: #ff4b4b; font-weight: bold; }
    .cor-p { color: #ffffff; font-weight: bold; text-decoration: underline; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'l_sinais' not in st.session_state: st.session_state.l_sinais = []

# --- MOTOR DE INTERVALOS (4-2-3) ---
def gerar_6_sinais(h_inicio, m_inicio, cor_inicio):
    # Converte o input para objeto de tempo
    agora = datetime.now(fuso_ms)
    referencia = agora.replace(hour=h_inicio, minute=m_inicio, second=0, microsecond=0)
    
    # Se o horário já passou, assume que é para a próxima hora
    if referencia < agora - timedelta(minutes=10):
        referencia += timedelta(hours=1)
        
    # Sequência extraída das suas listas de 100%: 4 min, depois 2 min, depois 3 min
    pulos = [0, 4, 2, 3, 4, 2] 
    
    lista = []
    cor_atual = cor_inicio
    
    for i in range(6):
        referencia += timedelta(minutes=pulos[i])
        lista.append({
            "h": referencia.strftime("%H:%M"),
            "cor": cor_atual
        })
        # Alternância Automática de Cor
        cor_atual = "PRETO ⚫" if cor_atual == "VERMELHO 🔴" else "VERMELHO 🔴"
        
    return lista

# --- INTERFACE ---
st.title("🏹 SNIPER MS - TESTE DE INTERVALOS")

col_lista, col_ctrl = st.columns([1.5, 1])

with col_ctrl:
    st.markdown('<div class="box-setup">', unsafe_allow_html=True)
    st.subheader("⚙️ CONFIGURAR LISTA")
    
    c_hora, c_min = st.columns(2)
    h_ini = c_hora.number_input("HORA:", 0, 23, datetime.now(fuso_ms).hour)
    m_ini = c_min.number_input("MINUTO:", 0, 59, datetime.now(fuso_ms).minute)
    
    cor_ini = st.selectbox("COR DE INÍCIO:", ["VERMELHO 🔴", "PRETO ⚫"])
    
    if st.button("🔥 GERAR 6 SINAIS AGORA", use_container_width=True):
        st.session_state.l_sinais = gerar_6_sinais(h_ini, m_ini, cor_ini)
        st.rerun()

    if st.button("🗑️ LIMPAR", use_container_width=True):
        st.session_state.l_sinais = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.info("Intervalos aplicados: +4, +2, +3, +4, +2 (Padrão Bear 100%)")

with col_lista:
    if st.session_state.l_sinais:
        st.subheader("🎯 LISTA DE ENTRADAS")
        for s in st.session_state.l_sinais:
            cor_borda = "#ff4b4b" if "🔴" in s['cor'] else "#ffffff"
            st.markdown(f'''
                <div class="card-sinal" style="border-left-color: {cor_borda};">
                    <span style="font-size: 24px;">⏰ {s["h"]} | <b>{s["cor"]}</b></span>
                    <br><small>Proteção no Branco ⚪</small>
                </div>
            ''', unsafe_allow_html=True)
