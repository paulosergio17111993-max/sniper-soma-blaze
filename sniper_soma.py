import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - ESTÁVEL", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-alerta { 
        background: #161b22; border: 2px solid #00ff88; padding: 15px; 
        border-radius: 10px; text-align: center; margin-bottom: 20px;
    }
    .radar-box { 
        background-color: #10141d; border: 1px solid #1d2633; border-radius: 8px; 
        padding: 12px; margin-bottom: 8px; border-left: 5px solid #00ff88; font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA SEGURA ---
if 'l_sinais' not in st.session_state: 
    st.session_state.l_sinais = []

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
        
    nova_lista = []
    cor_atual = cor_inicial
    
    for i in range(4):
        nova_lista.append({
            "horario": referencia.strftime("%H:%M"), 
            "cor_entrada": cor_atual,
            "branco_entrada": "BRANCO ⚪"
        })
        # Alternância de Cor
        cor_atual = "PRETO ⚫" if cor_atual == "VERMELHO 🔴" else "VERMELHO 🔴"
        referencia += timedelta(minutes=4)
    return nova_lista

# --- INTERFACE ---
st.title("🎯 SNIPER MS - OPERAÇÃO")

col_listas, col_ctrl = st.columns([2, 1])

with col_ctrl:
    st.subheader("⌨️ DADOS DA MESA")
    p_atual = st.number_input("PEDRA QUE SAIU:", 0, 14, 7)
    m_atual = st.number_input("MINUTO ATUAL:", 0, 59, 20)
    
    # Cálculo: Minuto + Pedra
    min_calc = (m_atual + p_atual) % 60
    cor_ini = calcular_primeira_cor(p_atual)
    
    st.markdown(f"""
        <div class="box-alerta">
            <small>PRÓXIMA ENTRADA:</small><br>
            <h2 style="color:#00ff88; margin:0;">{cor_ini}</h2>
            <h3 style="margin:0;">No Minuto: :{min_calc:02d}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ GERAR LISTAS (4 SINAIS)", use_container_width=True):
        # Limpa a memória antiga para evitar o KeyError
        st.session_state.l_sinais = gerar_ciclo_completo(min_calc, cor_ini)
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_sinais = []
        st.rerun()

with col_listas:
    if st.session_state.l_sinais:
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("🔥 CORES")
            for s in st.session_state.l_sinais:
                # Segurança: verifica se a chave existe antes de usar
                cor_txt = s.get('cor_entrada', 'N/A')
                borda = "#ff4b4b" if "🔴" in cor_txt else "#444"
                st.markdown(f'<div class="radar-box" style="border-left-color:{borda};">⏰ {s["horario"]} | {cor_txt}</div>', unsafe_allow_html=True)

        with c2:
            st.subheader("⚪ BRANCOS")
            for s in st.session_state.l_sinais:
                st.markdown(f'<div class="radar-box" style="border-left-color:#fff;">⏰ {s["horario"]} | BRANCO ⚪</div>', unsafe_allow_html=True)
