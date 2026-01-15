import streamlit as st
from datetime import datetime, timedelta
import pytz

fuso_ms = pytz.timezone('America/Campo_Grande')
st.set_page_config(page_title="SNIPER MS - CONTADOR", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .card-sinal { 
        background: #161b22; border-radius: 12px; padding: 15px; 
        margin-bottom: 10px; border-left: 10px solid #00ff88;
    }
    .contador-box {
        background: #0d1117; border: 1px solid #30363d; padding: 20px;
        border-radius: 15px; text-align: center; border-top: 4px solid #00ff88;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DOS ACERTOS ---
if 'placar' not in st.session_state:
    st.session_state.placar = {"SG": 0, "G1": 0, "G2": 0, "LOSS": 0}

# --- INTERFACE ---
st.title("🎯 SNIPER MS - ESTRATÉGIA 3-9-12")

col_lista, col_stats = st.columns([1.5, 1])

with col_stats:
    st.markdown('<div class="contador-box">', unsafe_allow_html=True)
    st.subheader("📊 CONTADOR DE CICLO")
    
    # Exibição do Placar
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SG", st.session_state.placar["SG"])
    c2.metric("G1", st.session_state.placar["G1"])
    c3.metric("G2", st.session_state.placar["G2"])
    c4.metric("LOSS", st.session_state.placar["LOSS"], delta_color="inverse")
    
    st.write("---")
    st.write("📝 **REGISTRAR RESULTADO:**")
    bt1, bt2 = st.columns(2)
    if bt1.button("✅ VITÓRIA SG", use_container_width=True):
        st.session_state.placar["SG"] += 1
        st.rerun()
    if bt2.button("❌ LOSS", use_container_width=True):
        st.session_state.placar["LOSS"] += 1
        st.rerun()
        
    if st.button("🔄 ZERAR CONTADOR", use_container_width=True):
        st.session_state.placar = {"SG": 0, "G1": 0, "G2": 0, "LOSS": 0}
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_lista:
    st.subheader("🕵️ GERADOR ESPELHO :00")
    cor_00 = st.selectbox("QUAL COR NO MINUTO :00?", ["VERMELHO 🔴", "PRETO ⚫"])
    
    if st.button("🚀 GERAR 3-9-12", use_container_width=True):
        agora = datetime.now(fuso_ms)
        ref = agora.replace(minute=0, second=0, microsecond=0)
        if agora.minute > 15: ref += timedelta(hours=1)
        
        st.session_state.sinais_v3 = []
        for m in [3, 9, 12]:
            h_sinal = ref + timedelta(minutes=m)
            st.session_state.sinais_v3.append({"h": h_sinal.strftime("%H:%M"), "c": cor_00})

    if 'sinais_v3' in st.session_state:
        st.write("---")
        for s in st.session_state.sinais_v3:
            cor_b = "#ff4b4b" if "🔴" in s['c'] else "#ffffff"
            st.markdown(f'''
                <div class="card-sinal" style="border-left-color: {cor_b};">
                    <span style="font-size:22px;">⏰ {s["h"]} | ENTRAR EM: <b>{s["c"]}</b></span>
                </div>
            ''', unsafe_allow_html=True)

st.info("💡 Dica: Se o contador marcar 2 LOSS seguidos na hora, pare a operação. A mesa mudou o padrão.")
