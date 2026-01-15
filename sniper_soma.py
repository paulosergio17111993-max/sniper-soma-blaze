import streamlit as st
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO ---
fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - OFICIAL", layout="wide")

# --- ESTILO VISUAL (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px; border-left: 10px solid #00ff88;
        display: flex; justify-content: space-between; align-items: center;
    }
    .main-box {
        background: #0d1117; border: 2px solid #30363d; padding: 25px; 
        border-radius: 15px; margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%; border-radius: 8px; font-weight: bold; height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "G1": 0, "LOSS": 0}
if 'lista_ativa' not in st.session_state:
    st.session_state.lista_ativa = []

# --- BARRA LATERAL (PLACAR) ---
with st.sidebar:
    st.markdown("### 📊 PLACAR DE HOJE")
    c1, c2, c3 = st.columns(3)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("G1", st.session_state.placar["G1"])
    c3.metric("LOSS", st.session_state.placar["LOSS"])
    
    st.markdown("---")
    if st.button("✅ VITÓRIA SG"): st.session_state.placar["SG"] += 1; st.rerun()
    if st.button("🟡 VITÓRIA G1"): st.session_state.placar["G1"] += 1; st.rerun()
    if st.button("❌ LOSS"): st.session_state.placar["LOSS"] += 1; st.rerun()
    if st.button("🔄 ZERAR TUDO"): st.session_state.placar = {"SG": 0, "G1": 0, "LOSS": 0}; st.rerun()

# --- PAINEL PRINCIPAL ---
st.title("🏹 SNIPER MS - CENTRAL DE OPERAÇÕES")

# ABAS ORGANIZADAS
tab_espelho, tab_pedra, tab_bear = st.tabs([
    "💎 PADRÃO ESPELHO (3-9-12)", 
    "🎲 CÁLCULO POR PEDRA", 
    "🎯 PADRÃO BEAR (4-2-3)"
])

# 1. ABA ESPELHO (LÓGICA MINUTO :00)
with tab_espelho:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🕵️ Lógica de Repetição do Minuto :00")
    cor_00 = st.selectbox("Cor que saiu no :00:", ["VERMELHO 🔴", "PRETO ⚫"], key="sel_00")
    
    if st.button("🚀 GERAR CICLO 3-9-12"):
        # Baseado no seu padrão: Repete a cor do :00 nos minutos :03, :09 e :12
        ref = datetime.now(fuso_ms).replace(minute=0, second=0)
        if datetime.now(fuso_ms).minute > 15: ref += timedelta(hours=1)
        
        st.session_state.lista_ativa = []
        for m in [3, 9, 12]:
            hora_s = ref + timedelta(minutes=m)
            st.session_state.lista_ativa.append({"h": hora_s.strftime("%H:%M"), "c": cor_00, "t": "SG"})
    st.markdown('</div>', unsafe_allow_html=True)

# 2. ABA PEDRA (MINUTO + PEDRA)
with tab_pedra:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🔢 Cálculo Simétrico")
    col1, col2 = st.columns(2)
    p_valor = col1.number_input("Pedra que saiu:", 0, 14, 7)
    m_relogio = col2.number_input("Minuto do Relógio:", 0, 59, datetime.now(fuso_ms).minute)
    
    m_calc = (p_valor + m_relogio) % 60
    st.info(f"O sinal calculado começa no minuto: **:{m_calc:02d}**")
    
    if st.button("🚀 GERAR POR PEDRA"):
        st.session_state.lista_ativa = [{"h": f"00:{m_calc:02d}", "c": "ANALISANDO...", "t": "SG"}]
    st.markdown('</div>', unsafe_allow_html=True)

# 3. ABA BEAR (PADRÃO +4, +2, +3...)
with tab_bear:
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    st.subheader("🎯 Padrão Bear 100%")
    c_hora, c_min, c_cor = st.columns(3)
    h_b = c_hora.number_input("Hora:", 0, 23, datetime.now(fuso_ms).hour)
    m_b = c_min.number_input("Minuto:", 0, 59, datetime.now(fuso_ms).minute)
    cor_b = c_cor.selectbox("Cor Início:", ["VERMELHO 🔴", "PRETO ⚫"])
    
    if st.button("🚀 GERAR SEQUÊNCIA BEAR"):
        # Intervalos aplicados: +4, +2, +3, +4, +2
        pulos = [0, 4, 2, 3, 4, 2]
        ref_b = datetime.now(fuso_ms).replace(hour=h_b, minute=m_b, second=0)
        st.session_state.lista_ativa = []
        c_at = cor_b
        for p in pulos:
            ref_b += timedelta(minutes=p)
            st.session_state.lista_ativa.append({"h": ref_b.strftime("%H:%M"), "c": c_at, "t": "SG"})
            c_at = "PRETO ⚫" if c_at == "VERMELHO 🔴" else "VERMELHO 🔴"
    st.markdown('</div>', unsafe_allow_html=True)

# --- ÁREA DE RESULTADOS (LISTA GERADA) ---
if st.session_state.lista_ativa:
    st.markdown("### 🔥 SINAIS PARA OPERAÇÃO")
    for s in st.session_state.lista_ativa:
        cor_layout = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
        st.markdown(f'''
            <div class="card-sinal" style="border-left-color: {cor_layout};">
                <span style="font-size: 22px;">⏰ <b>{s['h']}</b> | {s['c']}</span>
                <span style="background:#00ff88; color:black; padding:3px 8px; border-radius:5px; font-weight:bold;">{s['t']}</span>
            </div>
        ''', unsafe_allow_html=True)
