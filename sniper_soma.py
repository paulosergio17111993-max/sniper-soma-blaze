import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .info-inicio { 
        background: #0d1117; border: 2px solid #00ff88; padding: 25px; 
        border-radius: 15px; text-align: center; margin-top: 10px;
    }
    .card-sinal { 
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 12px; border-left: 10px solid #00ff88;
        display: flex; justify-content: space-between; align-items: center;
    }
    .texto-sinal { font-size: 26px; font-weight: bold; }
    .horario-sinal { color: #8b949e; font-size: 18px; margin-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

if 'l_sinais' not in st.session_state: st.session_state.l_sinais = []

# --- MOTOR COM VOLTA DA PEDRA E INTERVALOS 4-2-3 ---
def gerar_sequencia_pedra(min_calc, cor_ini):
    agora = datetime.now(fuso_ms)
    # Define o primeiro horário com base no cálculo da pedra
    referencia = agora.replace(minute=min_calc, second=0, microsecond=0)
    
    if referencia < agora - timedelta(minutes=2):
        referencia += timedelta(hours=1)
        
    pulos = [0, 4, 2, 3, 4, 2] 
    sinais_calculados = []
    cor_atual = cor_ini
    
    for p in pulos:
        referencia += timedelta(minutes=p)
        sinais_calculados.append({
            "hora": referencia.strftime("%H:%M"),
            "cor": cor_atual
        })
        cor_atual = "PRETO ⚫" if cor_atual == "VERMELHO 🔴" else "VERMELHO 🔴"
        
    return sinais_calculados

# --- INTERFACE ---
st.title("🎯 SNIPER MS - MODO PEDRA")

col_lista, col_dados = st.columns([1.6, 1])

with col_dados:
    st.subheader("⌨️ DADOS DA MESA")
    
    # VOLTA DOS CAMPOS DE PEDRA E MINUTO
    pedra = st.number_input("PEDRA QUE SAIU:", 0, 14, 7)
    minuto_relogio = st.number_input("MINUTO DO RELÓGIO:", 0, 59, datetime.now(fuso_ms).minute)
    
    # Cálculo oficial: Minuto + Pedra
    min_final = (minuto_relogio + pedra) % 60
    
    # Regra de Cor pela Pedra
    cor_sugerida = "VERMELHO 🔴" if 1 <= pedra <= 7 else "PRETO ⚫" if 8 <= pedra <= 14 else "BRANCO ⚪"
    
    st.markdown(f"""
        <div class="info-inicio">
            <small>INÍCIO CALCULADO:</small><br>
            <h1 style="color:#00ff88; margin:5px 0;">{cor_sugerida.split(' ')[0]}</h1>
            <h2 style="margin:0;">Horário: :{min_final:02d}</h2>
            <p style="font-size:12px; color:#8b949e;">Soma: {minuto_relogio} + {pedra}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ GERAR LISTA (PADRÃO 4-2-3)", use_container_width=True):
        st.session_state.l_sinais = gerar_sequencia_pedra(min_final, cor_sugerida)
        st.rerun()

    if st.button("🗑️ LIMPAR", use_container_width=True):
        st.session_state.l_sinais = []
        st.rerun()

with col_lista:
    if st.session_state.l_sinais:
        st.subheader("🔥 SINAIS GERADOS")
        for s in st.session_state.l_sinais:
            cor_borda = "#ff4b4b" if "🔴" in s['cor'] else "#ffffff"
            st.markdown(f'''
                <div class="card-sinal" style="border-left-color: {cor_borda};">
                    <div class="texto-sinal">
                        <span class="horario-sinal">⏰ {s['hora']}</span> | {s['cor']} + ⚪
                    </div>
                </div>
            ''', unsafe_allow_html=True)
