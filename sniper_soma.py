import streamlit as st
import random
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="SNIPER SOMA 99%", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .placa-card { background: #1a2026; padding: 15px; border-radius: 10px; text-align: center; border-bottom: 4px solid #333; }
    .sinal-box { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border: 1px solid #30363d; }
    .numero-puxador { background: #f7b924; color: black; padding: 5px 12px; border-radius: 4px; font-weight: bold; margin-right: 5px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA ---
if 'lista_cores' not in st.session_state: st.session_state.lista_cores = []
if 'lista_brancos' not in st.session_state: st.session_state.lista_brancos = []
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0
if 'pedra_atual' not in st.session_state: st.session_state.pedra_atual = 12

# --- FUNÇÕES DE GERAÇÃO ---
def gerar_horarios(tipo):
    novos_horarios = []
    agora = datetime.now()
    for i in range(5):
        horario = (agora + timedelta(minutes=random.randint(2, 15))).strftime("%H:%M")
        if tipo == "cor":
            cor = random.choice(["VERMELHO 🔴", "PRETO ⚫"])
            novos_horarios.append({"h": horario, "c": cor})
        else:
            novos_horarios.append({"h": horario, "c": "BRANCO ⚪"})
    return novos_horarios

# --- CABEÇALHO: PLACA DE RESULTADOS ---
st.markdown("### 📊 PLACA DE RESULTADOS")
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="placa-card" style="border-color: #00ff88;"><b style="color: #00ff88;">SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="placa-card" style="border-color: #00d4ff;"><b style="color: #00d4ff;">G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="placa-card" style="border-color: #ff4d4d;"><b style="color: #ff4d4d;">LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="placa-card" style="border-color: #f7b924;"><b style="color: #f7b924;">TOTAL ACERTOS</b><br><h2>{st.session_state.sg + st.session_state.g1}</h2></div>', unsafe_allow_html=True)

st.divider()

# --- BARRA LATERAL: CONTROLES ---
with st.sidebar:
    st.header("🎮 CONTROLES")
    if st.button("🔄 GERAR LISTA DE CORES"):
        st.session_state.lista_cores = gerar_horarios("cor")
    
    if st.button("⚪ GERAR LISTA DE BRANCOS"):
        st.session_state.lista_brancos = gerar_horarios("branco")
    
    st.divider()
    nova_pedra = st.number_input("DIGITAR PEDRA ATUAL:", min_value=0, max_value=14, value=st.session_state.pedra_atual)
    if nova_pedra != st.session_state.pedra_atual:
        st.session_state.pedra_atual = nova_pedra
        st.rerun()

    if st.button("🗑️ ZERAR TUDO"):
        st.session_state.sg = 0
        st.session_state.g1 = 0
        st.session_state.loss = 0
        st.session_state.lista_cores = []
        st.session_state.lista_brancos = []
        st.rerun()

# --- CORPO PRINCIPAL ---
col_sinais, col_analise = st.columns([2, 1])

with col_sinais:
    if st.session_state.lista_cores:
        st.markdown("### 📋 RADAR DE CORES")
        for s in st.session_state.lista_cores:
            col_t, col_b = st.columns([3, 2])
            col_t.markdown(f'<div class="sinal-box">⏰ {s["h"]} | {s["c"]}</div>', unsafe_allow_html=True)
            b1, b2, b3 = col_b.columns(3)
            if b1.button("SG", key=f"sg_{s['h']}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"g1_{s['h']}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"l_{s['h']}"): st.session_state.loss += 1; st.rerun()

    if st.session_state.lista_brancos:
        st.markdown("### ⚪ RADAR DE BRANCOS")
        for b in st.session_state.lista_brancos:
            st.markdown(f'<div class="sinal-box" style="border-left: 5px solid white;">⏰ {b["h"]} | {b["c"]}</div>', unsafe_allow_html=True)

with col_analise:
    st.markdown("### 🧮 ANÁLISE DA SOMA")
    cor_nome = "PRETO ⚫" if st.session_state.pedra_atual >= 8 else "VERMELHO 🔴"
    if st.session_state.pedra_atual == 0: cor_nome = "BRANCO ⚪"
    
    st.markdown(f"""
    <div style="background: #1a2026; padding: 20px; border-radius: 10px; border: 1px solid #333;">
        <p><b>PEDRA ATUAL:</b> <span style="font-size:30px; color:#f7b924;">{st.session_state.pedra_atual}</span></p>
        <p><b>COR:</b> {cor_nome}</p>
        <p><b>SOMA ANALISADA:</b> {st.session_state.pedra_atual}</p>
        <hr>
        <p><b>PUXADORES ATIVOS:</b></p>
        <span class="numero-puxador">4</span> 
        <span class="numero-puxador">12</span> 
        <span class="numero-puxador">7</span>
    </div>
    """, unsafe_allow_html=True)
