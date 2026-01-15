import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO LIMPO E PROFISSIONAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    
    /* Box de Informação de Início */
    .info-inicio { 
        background: #0d1117; border: 2px solid #00ff88; padding: 25px; 
        border-radius: 15px; text-align: center; margin-top: 10px;
    }
    
    /* Cards dos Sinais */
    .card-sinal { 
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 12px; border-left: 10px solid #00ff88;
        display: flex; justify-content: space-between; align-items: center;
    }
    
    .texto-sinal { font-size: 26px; font-weight: bold; }
    .horario-sinal { color: #8b949e; font-size: 18px; margin-right: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if 'l_sinais' not in st.session_state: 
    st.session_state.l_sinais = []

# --- MOTOR DE INTELIGÊNCIA (INTERVALOS 4-2-3-4-2) ---
def gerar_sequencia_vitoriosa(h_ini, m_ini, cor_ini):
    agora = datetime.now(fuso_ms)
    referencia = agora.replace(hour=h_ini, minute=m_ini, second=0, microsecond=0)
    
    if referencia < agora - timedelta(minutes=5):
        referencia += timedelta(hours=1)
        
    # Intervalos Sanfona: Começa no tempo 0, depois pula 4, 2, 3, 4, 2
    pulos = [0, 4, 2, 3, 4, 2] 
    sinais_calculados = []
    cor_atual = cor_ini
    
    for p in pulos:
        referencia += timedelta(minutes=p)
        sinais_calculados.append({
            "hora": referencia.strftime("%H:%M"),
            "cor": cor_atual
        })
        # Alternância de Cor Automática
        cor_atual = "PRETO ⚫" if cor_atual == "VERMELHO 🔴" else "VERMELHO 🔴"
        
    return sinais_calculados

# --- INTERFACE ---
st.title("🎯 SNIPER MS - MODO ESTRATÉGICO")

col_lista, col_dados = st.columns([1.6, 1])

with col_dados:
    st.subheader("⌨️ DADOS DA MESA")
    
    h_atual = datetime.now(fuso_ms).hour
    m_atual = datetime.now(fuso_ms).minute
    
    c1, c2 = st.columns(2)
    h_input = c1.number_input("HORA:", 0, 23, h_atual)
    m_input = c2.number_input("MINUTO:", 0, 59, m_atual)
    
    cor_escolhida = st.selectbox("COR DE INÍCIO:", ["VERMELHO 🔴", "PRETO ⚫"])
    
    # Painel de Preview do Início
    st.markdown(f"""
        <div class="info-inicio">
            <small>INÍCIO DA SEQUÊNCIA:</small><br>
            <h1 style="color:#00ff88; margin:5px 0;">{cor_escolhida.split(' ')[0]}</h1>
            <h2 style="margin:0;">Horário: :{m_input:02d}</h2>
            <p style="font-size:12px; color:#8b949e;">A lista seguirá o padrão de alternância</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") # Espaçamento
    
    if st.button("➕ GERAR LISTA DE SINAIS", use_container_width=True):
        st.session_state.l_sinais = gerar_sequencia_vitoriosa(h_input, m_input, cor_escolhida)
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_sinais = []
        st.rerun()

with col_lista:
    if st.session_state.l_sinais:
        st.subheader("🔥 SINAIS GERADOS")
        for s in st.session_state.l_sinais:
            # Pega as informações com segurança
            horario = s.get("hora", "00:00")
            cor_final = s.get("cor", "BRANCO ⚪")
            
            # Define a cor da borda lateral
            cor_borda = "#ff4b4b" if "🔴" in cor_final else "#ffffff"
            
            st.markdown(f'''
                <div class="card-sinal" style="border-left-color: {cor_borda};">
                    <div class="texto-sinal">
                        <span class="horario-sinal">⏰ {horario}</span> | {cor_final} + ⚪
                    </div>
                </div>
            ''', unsafe_allow_html=True)
