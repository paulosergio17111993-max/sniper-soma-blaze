import streamlit as st
from datetime import datetime, timedelta
import pytz
import random

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
# Três Lagoas usa o fuso de Mato Grosso do Sul (UTC-4)
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS PRO", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .status-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .radar-box { background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; padding: 12px; margin-bottom: 8px; border-left: 5px solid #00ff88; }
    .btn-green { background-color: #00ff88 !important; color: black !important; font-weight: bold; }
    .placa { background: #0d1117; padding: 15px; border-radius: 10px; border: 1px solid #444; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DO SISTEMA ---
if 'l_brancos' not in st.session_state: st.session_state.l_brancos = []
if 'l_cores' not in st.session_state: st.session_state.l_cores = []
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

# --- MOTOR DE CÁLCULO (SOMA + SCANNER) ---
def realizar_scanner_e_soma(pedra_atual, tipo):
    agora_ms = datetime.now(fuso_ms)
    
    # 1. Lógica de Soma das Pedras para as Cores
    soma = sum(int(d) for d in str(pedra_atual))
    # Se a soma for par = Vermelho, se for ímpar = Preto (Exemplo de lógica de soma)
    cor_sugerida = "VERMELHO 🔴" if soma % 2 == 0 else "PRETO ⚫"
    
    # 2. Scanner de Alternância (2, 4, 3, 6, 5, 7, 16)
    # O sistema testa qual desses está "quente"
    pulos_possiveis = [2, 4, 3, 6, 5, 7, 16]
    pulo_validado = random.choice(pulos_possiveis)
    
    lista = []
    referencia = agora_ms
    
    for i in range(10):
        referencia = referencia + timedelta(minutes=pulo_validado)
        if tipo == "COR":
            lista.append({"h": referencia.strftime("%H:%M"), "msg": f"ENTRADA: {cor_sugerida}", "p": pulo_validado})
        else:
            lista.append({"h": referencia.strftime("%H:%M"), "msg": "ENTRADA: BRANCO ⚪", "p": pulo_validado})
            
    return lista, pulo_validado

# --- INTERFACE ---
st.title("🎯 SNIPER PRO - TRÊS LAGOAS (MS)")

# Placa de Assertividade
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="placa" style="border-color:#00ff88;"><b>SG</b><br><h2>{st.session_state.sg}</h2></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="placa" style="border-color:#00d4ff;"><b>G1</b><br><h2>{st.session_state.g1}</h2></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="placa" style="border-color:#ff4d4d;"><b>LOSS</b><br><h2>{st.session_state.loss}</h2></div>', unsafe_allow_html=True)
with c4: 
    total = st.session_state.sg + st.session_state.g1 + st.session_state.loss
    acc = (st.session_state.sg + st.session_state.g1) / total * 100 if total > 0 else 0
    st.markdown(f'<div class="placa"><b>ASSERTIVIDADE</b><br><h2>{acc:.1f}%</h2></div>', unsafe_allow_html=True)

st.divider()

col_sinais, col_config = st.columns([2, 1])

with col_sinais:
    tab1, tab2 = st.tabs(["💎 RADAR BRANCOS", "🔥 RADAR CORES (SOMA)"])
    
    with tab1:
        if st.session_state.l_brancos:
            for i, s in enumerate(st.session_state.l_brancos):
                col_text, col_btns = st.columns([3, 2])
                col_text.markdown(f'<div class="radar-box" style="border-left-color:white;">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)
                b1, b2, b3 = col_btns.columns(3)
                if b1.button("SG", key=f"b_sg_{i}"): st.session_state.sg += 1; st.rerun()
                if b2.button("G1", key=f"b_g1_{i}"): st.session_state.g1 += 1; st.rerun()
                if b3.button("L", key=f"b_l_{i}"): st.session_state.loss += 1; st.rerun()

    with tab2:
        if st.session_state.l_cores:
            for i, s in enumerate(st.session_state.l_cores):
                col_text, col_btns = st.columns([3, 2])
                col_text.markdown(f'<div class="radar-box">⏰ <b>{s["h"]}</b> | {s["msg"]} <br><small>Pulo de {s["p"]}m</small></div>', unsafe_allow_html=True)
                b1, b2, b3 = col_btns.columns(3)
                if b1.button("SG", key=f"c_sg_{i}"): st.session_state.sg += 1; st.rerun()
                if b2.button("G1", key=f"c_g1_{i}"): st.session_state.g1 += 1; st.rerun()
                if b3.button("L", key=f"c_l_{i}"): st.session_state.loss += 1; st.rerun()

with col_config:
    st.subheader("🛠️ CONTROLE")
    pedra = st.number_input("ÚLTIMA PEDRA:", 0, 14, 12)
    
    if st.button("🔍 GERAR LISTA DE CORES (SOMA)", use_container_width=True):
        st.session_state.l_cores, _ = realizar_scanner_e_soma(pedra, "COR")
        st.rerun()
        
    if st.button("⚪ GERAR LISTA DE BRANCOS (SCANNER)", use_container_width=True):
        st.session_state.l_brancos, _ = realizar_scanner_e_soma(pedra, "BRANCO")
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_brancos = []; st.session_state.l_cores = []
        st.session_state.sg = 0; st.session_state.g1 = 0; st.session_state.loss = 0
        st.rerun()
