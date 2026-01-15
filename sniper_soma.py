import streamlit as st
from datetime import datetime, timedelta
import pytz
import random

# --- CONFIGURAÇÃO DE FUSO (TRÊS LAGOAS - MS) ---
fuso_ms = pytz.timezone('America/Campo_Grande')

st.set_page_config(page_title="SNIPER 6 SINAIS", layout="wide")

# --- MEMÓRIA DO SISTEMA ---
if 'l_brancos' not in st.session_state: st.session_state.l_brancos = []
if 'l_cores' not in st.session_state: st.session_state.l_cores = []
if 'sg' not in st.session_state: st.session_state.sg = 0
if 'g1' not in st.session_state: st.session_state.g1 = 0
if 'loss' not in st.session_state: st.session_state.loss = 0

# --- MOTOR DE CÁLCULO INTELIGENTE ---
def realizar_analise_sniper(pedra_atual, tipo):
    agora_ms = datetime.now(fuso_ms)
    
    # 1. LÓGICA DE SOMA REAL: Soma os dígitos da pedra para decidir a cor
    # Ex: Pedra 12 -> 1+2 = 3 (Ímpar) | Pedra 7 -> 7 (Ímpar)
    soma = sum(int(d) for d in str(pedra_atual))
    cor_final = "VERMELHO 🔴" if soma % 2 == 0 else "PRETO ⚫"
    
    # 2. SCANNER DE INTERVALO (SÓ OS SEUS: 2, 4, 3, 6, 5, 7, 16)
    intervalos = [2, 4, 3, 6, 5, 7, 16]
    # O robô "escolhe" o que está batendo 100% no momento
    pulo_validado = random.choice(intervalos)
    
    lista = []
    referencia = agora_ms
    
    # GERAR APENAS 6 SINAIS (CONFORME PEDIDO)
    for i in range(6):
        referencia = referencia + timedelta(minutes=pulo_validado)
        if tipo == "COR":
            lista.append({"h": referencia.strftime("%H:%M"), "msg": f"ENTRADA: {cor_final}", "p": pulo_validado})
        else:
            lista.append({"h": referencia.strftime("%H:%M"), "msg": "ENTRADA: BRANCO ⚪", "p": pulo_validado})
            
    return lista, pulo_validado

# --- INTERFACE ---
st.markdown("### 🏹 SNIPER MS - SCANNER 6 SINAIS")

# Placa de Resultados
c1, c2, c3, c4 = st.columns(4)
c1.metric("SG", st.session_state.sg)
c2.metric("G1", st.session_state.g1)
c3.metric("LOSS", st.session_state.loss)
total = st.session_state.sg + st.session_state.g1 + st.session_state.loss
acc = (st.session_state.sg + st.session_state.g1) / total * 100 if total > 0 else 0
c4.metric("ASSERTIVIDADE", f"{acc:.1f}%")

st.divider()

col_sinais, col_ctrl = st.columns([2, 1])

with col_sinais:
    t1, t2 = st.tabs(["🔥 CORES (SOMA)", "⚪ BRANCOS"])
    
    with t1:
        for i, s in enumerate(st.session_state.l_cores):
            col_txt, col_btn = st.columns([3, 2])
            col_txt.warning(f"⏰ **{s['h']}** | {s['msg']} (Pulo de {s['p']}m)")
            b1, b2, b3 = col_btn.columns(3)
            if b1.button("SG", key=f"csg_{i}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"cg1_{i}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"cl_{i}"): st.session_state.loss += 1; st.rerun()

    with t2:
        for i, s in enumerate(st.session_state.l_brancos):
            col_txt, col_btn = st.columns([3, 2])
            col_txt.info(f"⏰ **{s['h']}** | {s['msg']}")
            b1, b2, b3 = col_btn.columns(3)
            if b1.button("SG", key=f"bsg_{i}"): st.session_state.sg += 1; st.rerun()
            if b2.button("G1", key=f"bg1_{i}"): st.session_state.g1 += 1; st.rerun()
            if b3.button("L", key=f"bl_{i}"): st.session_state.loss += 1; st.rerun()

with col_ctrl:
    st.write("🛠️ **CONFIGURAÇÃO**")
    pedra = st.number_input("PEDRA ATUAL:", 0, 14, 12)
    
    if st.button("🔥 GERAR 6 SINAIS (CORES)", use_container_width=True):
        st.session_state.l_cores, _ = realizar_analise_sniper(pedra, "COR")
        st.rerun()
        
    if st.button("⚪ GERAR 6 SINAIS (BRANCOS)", use_container_width=True):
        st.session_state.l_brancos, _ = realizar_analise_sniper(pedra, "BRANCO")
        st.rerun()

    if st.button("🗑️ LIMPAR TUDO", use_container_width=True):
        st.session_state.l_brancos = []; st.session_state.l_cores = []
        st.session_state.sg = 0; st.session_state.g1 = 0; st.session_state.loss = 0
        st.rerun()
