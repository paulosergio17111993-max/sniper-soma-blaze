import streamlit as st
from datetime import datetime, timedelta
import pytz
import random

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER MS - COMPLETO", layout="wide")

# --- MEMÓRIA (CADA UMA NA SUA) ---
if 'l_cores' not in st.session_state: st.session_state.l_cores = []
if 'l_brancos' not in st.session_state: st.session_state.l_brancos = []
if 'cor_soma' not in st.session_state: st.session_state.cor_soma = "Aguardando..."
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e11; color: white; }
    .box-soma { background: #161b22; border: 2px solid #00ff88; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .radar-box { background-color: #10141d; border: 1px solid #1d2633; border-radius: 10px; padding: 10px; margin-bottom: 5px; border-left: 5px solid #00ff88; }
    .placa { background: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #444; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES ---

def soma_das_pedras(p):
    # Lógica de Soma: Soma os dígitos e define a cor
    s = sum(int(d) for d in str(p))
    return "VERMELHO 🔴" if s % 2 == 0 else "PRETO ⚫"

def gerar_sinais(tipo):
    agora = datetime.now(fuso_ms)
    # Lista de intervalos que você passou
    pulos = [2, 3, 4, 5, 6, 7, 16]
    pulo_escolhido = random.choice(pulos)
    
    lista = []
    referencia = agora
    for i in range(6):
        referencia = referencia + timedelta(minutes=pulo_escolhido)
        if tipo == "COR":
            # Pega a cor baseada na soma da pedra atual no momento da geração
            cor = soma_das_pedras(st.session_state.pedra_input)
            lista.append({"h": referencia.strftime("%H:%M"), "msg": f"ENTRADA: {cor}", "p": pulo_escolhido})
        else:
            lista.append({"h": referencia.strftime("%H:%M"), "msg": "ENTRADA: BRANCO ⚪", "p": pulo_escolhido})
    return lista

# --- INTERFACE ---
st.title("🎯 SNIPER MS - PAINEL INDEPENDENTE")

# Placa de Resultados
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="placa"><b>SG</b><br><h3>{st.session_state.sg}</h3></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="placa"><b>G1</b><br><h3>{st.session_state.g1}</h3></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="placa"><b>LOSS</b><br><h3>{st.session_state.loss}</h3></div>', unsafe_allow_html=True)
with c4: 
    total = st.session_state.sg + st.session_state.g1 + st.session_state.loss
    acc = (st.session_state.sg + st.session_state.g1) / total * 100 if total > 0 else 100
    st.markdown(f'<div class="placa"><b>ASSERTIVIDADE</b><br><h3>{acc:.0f}%</h3></div>', unsafe_allow_html=True)

st.divider()

col_lista, col_ctrl = st.columns([2, 1])

with col_ctrl:
    st.subheader("⚙️ CONFIGURAÇÃO")
    st.session_state.pedra_input = st.number_input("ÚLTIMA PEDRA:", 0, 14, 12)
    
    # FUNÇÃO 1: SOMA DAS PEDRAS
    if st.button("🧮 ANALISAR SOMA DA PEDRA", use_container_width=True):
        st.session_state.cor_soma = soma_das_pedras(st.session_state.pedra_input)
    
    st.markdown(f'<div class="box-soma">COR PELA SOMA:<br><h2>{st.session_state.cor_soma}</h2></div>', unsafe_allow_html=True)

    # FUNÇÃO 2: GERAR LISTA DE CORES
    if st.button("🔥 GERAR 6 SINAIS (CORES)", use_container_width=True):
        st.session_state.l_cores = gerar_sinais("COR")
        st.rerun()

    # FUNÇÃO 3: GERAR LISTA DE BRANCOS
    if st.button("⚪ GERAR 6 SINAIS (BRANCOS)", use_container_width=True):
        st.session_state.l_brancos = gerar_sinais("BRANCO")
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_cores = []; st.session_state.l_brancos = []
        st.session_state.sg = 0; st.session_state.g1 = 0; st.session_state.loss = 0
        st.rerun()

with col_lista:
    # Exibe as listas separadas por blocos (cada uma na sua)
    if st.session_state.l_cores:
        st.subheader("🔥 RADAR DE CORES")
        for i, s in enumerate(st.session_state.l_cores):
            c_inf, c_res = st.columns([3, 2])
            c_inf.markdown(f'<div class="radar-box">⏰ <b>{s["h"]}</b> | {s["msg"]} | {s["p"]}m</div>', unsafe_allow_html=True)
            with c_res:
                b1, b2, b3 = st.columns(3)
                if b1.button("SG", key=f"csg{i}"): st.session_state.sg += 1; st.rerun()
                if b2.button("G1", key=f"cg1{i}"): st.session_state.g1 += 1; st.rerun()
                if b3.button("L", key=f"cl{i}"): st.session_state.loss += 1; st.rerun()

    if st.session_state.l_brancos:
        st.subheader("⚪ RADAR DE BRANCOS")
        for i, s in enumerate(st.session_state.l_brancos):
            c_inf, c_res = st.columns([3, 2])
            c_inf.markdown(f'<div class="radar-box" style="border-left-color:white;">⏰ <b>{s["h"]}</b> | {s["msg"]}</div>', unsafe_allow_html=True)
            with c_res:
                b1, b2, b3 = st.columns(3)
                if b1.button("SG", key=f"bsg{i}"): st.session_state.sg += 1; st.rerun()
                if b2.button("G1", key=f"bg1{i}"): st.session_state.g1 += 1; st.rerun()
                if b3.button("L", key=f"bl{i}"): st.session_state.loss += 1; st.rerun()
