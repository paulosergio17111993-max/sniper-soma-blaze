import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background-color: #161b22; border-radius: 12px; padding: 15px; 
        margin-bottom: 8px; border-left: 10px solid #00ff88;
        font-size: 20px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO SEGURA DO PLACAR (APENAS SG E LOSS) ---
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "LOSS": 0}
if 'lista_ativa' not in st.session_state:
    st.session_state.lista_ativa = []

# --- BARRA LATERAL (PLACAR SG) ---
with st.sidebar:
    st.markdown("### 📊 PLACAR SG")
    c1, c2 = st.columns(2)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("LOSS", st.session_state.placar["LOSS"])
    
    st.markdown("---")
    if st.button("✅ REGISTRAR SG"): 
        st.session_state.placar["SG"] += 1
        st.rerun()
    if st.button("❌ REGISTRAR LOSS"): 
        st.session_state.placar["LOSS"] += 1
        st.rerun()
    if st.button("🔄 ZERAR"): 
        st.session_state.placar = {"SG": 0, "LOSS": 0}
        st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🏹 SNIPER MS - CENTRAL DE OPERAÇÕES")

# ABAS CONFORME IMAGENS
tab1, tab2, tab3 = st.tabs(["💎 PADRÃO ESPELHO (3-9-12)", "🎲 CÁLCULO POR PEDRA", "🎯 PADRÃO 4-2-3"])

with tab1:
    st.subheader("🕵️ Lógica de Repetição do Minuto :00")
    cor_00 = st.selectbox("Cor que saiu no :00:", ["PRETO ⚫", "VERMELHO 🔴"])
    if st.button("🚀 GERAR 3-9-12"):
        ref = datetime.now(fuso_ms).replace(minute=0, second=0, microsecond=0)
        st.session_state.lista_ativa = []
        for p in [3, 9, 12]:
            hora_s = ref + timedelta(minutes=p)
            st.session_state.lista_ativa.append({"h": hora_s.strftime("%H:%M"), "c": cor_00})

with tab2:
    st.subheader("🔢 Cálculo: Minuto + Pedra")
    p_val = st.number_input("Pedra que saiu:", 0, 14, 7)
    m_rel = st.number_input("Minuto do Relógio:", 0, 59, datetime.now(fuso_ms).minute)
    m_calc = (p_val + m_rel) % 60
    if st.button("🚀 GERAR POR PEDRA"):
        st.session_state.lista_ativa = [{"h": f"Minuto :{m_calc:02d}", "c": "COR DO 00"}]

with tab3:
    st.subheader("🎯 Padrão Sequencial 4-2-3-4-2")
    c_h, c_m = st.columns(2)
    h_b = c_h.number_input("Hora:", 0, 23, 21)
    m_b = c_m.number_input("Minuto:", 0, 59, 2)
    c_ini = st.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"])
    
    if st.button("🚀 GERAR BEAR"):
        # Intervalos: +4, +2, +3, +4, +2
        pulos = [0, 4, 2, 3, 4, 2]
        ref_b = datetime.now(fuso_ms).replace(hour=h_b, minute=m_b, second=0, microsecond=0)
        st.session_state.lista_ativa = []
        c_at = c_ini
        for p in pulos:
            ref_b += timedelta(minutes=p)
            st.session_state.lista_ativa.append({"h": ref_b.strftime("%H:%M"), "c": c_at})
            c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"

# --- LISTA DE RESULTADOS ---
if st.session_state.lista_ativa:
    st.write("---")
    for s in st.session_state.lista_ativa:
        cor_b = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
        st.markdown(f'''
            <div class="card-sinal" style="border-left-color: {cor_b};">
                ⏰ {s['h']} | {s['c']}
            </div>
        ''', unsafe_allow_html=True)
